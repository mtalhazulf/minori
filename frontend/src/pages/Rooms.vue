<template>
  <q-page class="q-mx-xl">
    <div class="row"><Heading :title="'Gestione stanze'" /></div>
    <h6 class="q-ma-md">Ospiti non allocati</h6>
    <div
      class="row q-ma-md q-pa-md"
      style="
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-bottom: 40px;
        background-color: #f1f1f1;
        min-height: 100px;
        display: flex;
        justify-content: start;
        align-items: start;
        flex-direction: row;
      "
      @dragover.prevent
      @dragenter.prevent
      @drop="onDrop($event, false)">
      <template v-if="minorsNotInRoom.length === 0">
        <q-item-label>Tutti gli ospiti sono stati allocati </q-item-label>
      </template>
      <template v-else>
        <MinorItem
          v-for="minor in minorsNotInRoom"
          :key="minor._id.$oid"
          :minor="minor"
          @dragstart="startDrag($event, minor, false)"
      /></template>
    </div>
    <div
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
      ">
      <h6 class="q-ma-md">Stanze</h6>
      <q-btn
        class="q-mr-md"
        label="Aggiungi stanza"
        color="primary"
        icon="add"
        @click="dialogAddRoom = true" />
    </div>
    <div
      v-if="rooms.length > 0"
      class="row q-ma-md q-pa-md"
      style="
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #f1f1f1;
        display: flex;
        justify-content: start;
        align-items: center;
      ">
      <div
        v-for="room in rooms"
        :key="room._id"
        class="column"
        style="
          display: flex;
          justify-content: start;
          align-items: center;
          flex-direction: column;
          margin: 0 10px 0 10px;
        ">
        <q-card
          class="room-box"
          @dragover.prevent
          @dragenter.prevent
          @mouseenter="
            () => {
              if (dragging === false) popups[room._id] = true
            }
          "
          @drop="onDrop($event, room)">
          <q-card-section style="padding-bottom: 5px !important">
            <q-item-label
              class="text-h6"
              style="
                font-weight: 500;
                background-image: linear-gradient(to left, #1976d2, #71b1e6);
                color: transparent;
                background-clip: text;
                -webkit-background-clip: text;
              ">
              {{ room.name }}
            </q-item-label>
          </q-card-section>
          <q-card-section style="padding: 17px 5px 17px 5px !important">
            <q-item v-if="room.guests.length === 0">
              <q-item-label
                style="
                  overflow: hidden;
                  text-overflow: ellipsis;
                  display: inline;
                ">
                Nessun ospite
              </q-item-label>
            </q-item>
            <q-list v-else>
              <q-item v-for="minor in room.guests" :key="minor._id.$oid" dense>
                <q-item-label
                  style="
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    display: block;
                  ">
                  {{ minor.name.charAt(0) + '. ' + minor.surname }}
                </q-item-label>
              </q-item>
            </q-list>
          </q-card-section>
          <q-separator style="margin-bottom: 15px" />
          <q-item>
            <q-item-label
              style="
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                display: block;
              "
              caption
              >{{ room.seats.available }} / {{ room.seats.total }} posti liberi
            </q-item-label>
          </q-item>
          <q-popup-proxy
            v-model="popups[room._id]"
            cover
            transition-show="jump-up"
            transition-hide="jump-down"
            style="transition-duration: 100ms"
            @mouseleave="
              () => {
                popups[room._id] = false
              }
            ">
            <q-card class="q-pa-md popup">
              <q-card-section
                style="
                  display: flex;
                  flex-direction: column;
                  justify-content: start;
                  align-items: center;
                ">
                <q-item-label class="text-h6 q-mb-sm">
                  {{ room.name }}
                </q-item-label>
                <q-item-label>
                  {{ room.seats.total }} posti totali</q-item-label
                >
                <q-item-label>
                  {{ room.seats.available }} posti liberi
                </q-item-label>
              </q-card-section>

              <q-card-section v-if="room.guests.length > 0">
                <q-item-label
                  class="text-h7 q-mb-md"
                  style="text-align: center">
                  Ospiti nella stanza
                </q-item-label>
                <MinorItem
                  v-for="minor in room.guests"
                  :key="minor"
                  :minor="minor"
                  fast-remove="true"
                  @remove="
                    () => {
                      editRoom({
                        _id: room._id,
                        name: room.name,
                        seats: room.seats,
                        guests: room.guests
                          .map(guest => guest._id)
                          .filter(guest => guest !== minor._id)
                      })
                    }
                  "
                  @dragstart="startDrag($event, minor, room)"
              /></q-card-section>
              <q-card-actions align="right">
                <q-btn
                  label="Modifica"
                  color="primary"
                  @click="editRoomDialog(room)" />
                <q-btn
                  label="Elimina"
                  color="negative"
                  @click="
                    askConfirm(
                      'Sei sicuro di voler eliminare la stanza?',
                      deleteRoom,
                      room._id
                    )
                  " />
              </q-card-actions>
            </q-card>
          </q-popup-proxy>
        </q-card>
      </div>
    </div>
    <h7 v-else class="q-ma-md"> Nessuna stanza </h7>

    <q-dialog v-model="dialogAddRoom" persistent>
      <q-card>
        <q-card-section>
          <q-item-label class="text-h6"
            >{{ isEditing ? 'Modifica' : 'Aggiungi' }} stanza</q-item-label
          >
        </q-card-section>
        <q-card-section>
          <q-input
            v-model="newRoomName"
            label="Nome stanza"
            outlined
            class="q-mb-md" />
          <q-input
            v-model="newRoomSeats"
            label="Posti totali"
            outlined
            type="number"
            min="1"
            class="q-mb-md" />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            label="Annulla"
            color="primary"
            flat
            @click="dialogAddRoom = false" />
          <q-btn
            :label="isEditing ? 'Modifica' : 'Aggiungi'"
            color="primary"
            @click="
              isEditing
                ? validateForm()
                  ? editRoom({
                      name: newRoomName,
                      seats: {
                        total: parseInt(newRoomSeats)
                      },
                      _id: currentRoomId,
                      guests: currentRoomGuests
                    })
                  : null
                : addRoom()
            " />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import Heading from 'components/Heading.vue'
import { useQuasar } from 'quasar'
import { api } from 'src/boot/axios'
import { ref, watch, onMounted } from 'vue'
import MinorItem from 'components/MinorItem.vue'

export default {
  name: 'Rooms',
  components: {
    Heading,
    MinorItem
  },
  setup() {
    const $q = useQuasar()

    const rooms = ref([])
    const minors = ref([])
    const minorsNotInRoom = ref([])
    const popups = ref([])
    const dragging = ref(false)
    const dialogAddRoom = ref(false)
    const newRoomName = ref('')
    const newRoomSeats = ref('')
    const isEditing = ref(false)
    const currentRoomId = ref('')
    const currentRoomGuests = ref([])

    watch(dialogAddRoom, newVal => {
      if (newVal === false) {
        newRoomName.value = ''
        newRoomSeats.value = ''
        isEditing.value = false
        currentRoomId.value = ''
      }
    })

    watch(rooms, newVal => {
      popups.value = newVal.reduce((acc, room) => {
        acc[room._id] = popups.value[room._id] || false
        return acc
      }, {})
    })

    watch([minors, rooms], ([newMinors, newRooms]) => {
      minorsNotInRoom.value = newMinors
        .filter(
          minor =>
            !newRooms.some(room =>
              room.guests.some(guest => guest._id === minor._id.$oid)
            )
        )
        .sort((a, b) => {
          if (a.surname < b.surname) return -1
          if (a.surname > b.surname) return 1
          if (a.name < b.name) return -1
          if (a.name > b.name) return 1
          return 0
        })
    })

    onMounted(() => {
      getRooms()
      getMinors()
    })

    function askConfirm(message, toExecute, ...args) {
      $q.dialog({
        title: 'Conferma',
        message: message || 'Sei sicuro di voler procedere',
        cancel: 'Annulla',
        persistent: true
      }).onOk(() => {
        toExecute(...args)
      })
    }

    function validateForm() {
      if (newRoomName.value === '') {
        showNotification('negative', 'Inserisci il nome della stanza')
        return false
      }
      if (newRoomSeats.value === '') {
        showNotification('negative', 'Inserisci il numero di posti')
        return false
      }
      return true
    }

    function editRoomDialog(room) {
      isEditing.value = true
      newRoomName.value = room.name
      newRoomSeats.value = room.seats.total
      currentRoomId.value = room._id
      currentRoomGuests.value = room.guests.map(guest => guest._id)
      dialogAddRoom.value = true
    }

    function showNotification(tp, msg) {
      $q.notify({
        type: tp,
        message: msg,
        position: 'top-right',
        timeout: 2000
      })
    }

    async function getRooms() {
      try {
        const response = await api.get('/rooms/room')
        rooms.value = response.data.rooms
      } catch (error) {
        showNotification('error', 'Errore durante il caricamento delle stanze')
      }
    }

    async function getMinors() {
      try {
        const response = await api.get('/minors/minor/all')
        minors.value = response.data
      } catch (error) {
        showNotification('warning', 'Errore durante il caricamento dei minori')
      }
    }

    async function editRoom(room) {
      try {
        await api.patch(`/rooms/room/${room._id}`, {
          name: room.name,
          guests: room.guests,
          seats: room.seats
        })
        getRooms()
        dialogAddRoom.value = false
        showNotification('positive', 'Modifica effettuata con successo')
      } catch (error) {
        showNotification('warning', 'Errore durante la modifica della stanza')
      }
    }

    async function deleteRoom(roomId) {
      try {
        await api.delete(`/rooms/room/${roomId}`)
        getRooms()
        showNotification('positive', 'Stanza eliminata con successo')
      } catch (error) {
        showNotification(
          'warning',
          "Errore durante l'eliminazione della stanza"
        )
      }
    }

    async function startDrag(ev, minor, fromRoom) {
      dragging.value = true
      ev.dataTransfer.dropEffect = 'move'
      ev.dataTransfer.effectAllowed = 'move'
      if (fromRoom) {
        popups.value[fromRoom._id] = false
        ev.dataTransfer.setData('room', JSON.stringify(fromRoom))
      }
      ev.dataTransfer.setData('minor', JSON.stringify(minor))
      ev.target.addEventListener('dragend', function () {
        dragging.value = false
      })
    }

    function onDrop(ev, room) {
      dragging.value = false
      const minor = JSON.parse(ev.dataTransfer.getData('minor'))
      let fromRoom
      try {
        fromRoom = JSON.parse(ev.dataTransfer.getData('room'))
      } catch (e) {
        fromRoom = null
      }
      if (room) {
        if (room._id === fromRoom?._id) {
          showNotification('warning', 'Il minore è già in questa stanza')
          return
        }
        if (room.seats.available <= 0) {
          showNotification('warning', 'La stanza è piena')
          return
        }
        const guestIds = room.guests.map(guest => guest._id)
        editRoom({
          _id: room._id,
          name: room.name,
          guests: [...guestIds, minor._id.$oid ?? minor._id],
          seats: room.seats
        })
      }
      if (fromRoom) {
        const guestIds = fromRoom.guests.map(guest => guest._id)
        editRoom({
          _id: fromRoom._id,
          name: fromRoom.name,
          guests: guestIds.filter(id => id !== minor._id),
          seats: fromRoom.seats
        })
      }
    }

    async function addRoom() {
      if (!validateForm()) return
      try {
        await api.post('/rooms/room', {
          name: newRoomName.value,
          seats: {
            total: parseInt(newRoomSeats.value)
          },
          guests: []
        })
        getRooms()
        dialogAddRoom.value = false
        showNotification('positive', 'Stanza aggiunta con successo')
      } catch (e) {
        showNotification('warning', "Errore durante l'aggiunta della stanza")
      }
    }

    return {
      rooms,
      minors,
      minorsNotInRoom,
      popups,
      dragging,
      dialogAddRoom,
      newRoomName,
      newRoomSeats,
      isEditing,
      currentRoomId,
      currentRoomGuests,
      showNotification,
      getRooms,
      getMinors,
      editRoom,
      startDrag,
      onDrop,
      addRoom,
      deleteRoom,
      validateForm,
      editRoomDialog,
      askConfirm
    }
  }
}
</script>

<style scoped>
.minor-box {
  margin: 5px;
  cursor: pointer;
  transition: 0.1s ease-in-out;
  overflow: auto;
  border-radius: 5px;
  border: 1px solid #ccc;
  color: black;
  background-color: #fff;
}
.minor-box:hover {
  transform: scale(1.1);
  transition: 0.1s ease-in-out;
}
.room-box {
  margin: 10px;
  cursor: pointer;
  width: 8vw;
  min-width: 80px;
  transition: 0.1s ease-in-out;
}

.popup {
  width: 100%;
  height: 100%;
  background-color: #a3c8f5;
  border: 1px solid #ccc;
  padding: 20px 15px 20px 15px;
  color: black;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
