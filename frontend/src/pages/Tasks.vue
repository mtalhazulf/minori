<template>
  <q-page class="q-mb-md q-mx-xl">
    <div class="row" style="height: 60px">
      <Heading :title="'Quaderno delle Consegne'" />
    </div>

    <div style="display: flex; align-items: center">
      <q-dialog v-model="info_dialog">
        <q-card>
          <q-card-section>
            <div class="row">
              <div class="col-11">
                <div class="text-h8">Dettagli Consegna</div>
                <div class="text-h6">
                  Consegna
                  {{
                    ('minor' in selectedTask &&
                      typeof selectedTask.minor === 'object' &&
                      selectedTask.minor?.name) ||
                    ('adult' in selectedTask &&
                      typeof selectedTask.adult === 'object' &&
                      selectedTask.adult?.name)
                      ? 'Personale'
                      : 'Generale'
                  }}
                </div>
              </div>
              <div class="col-1">
                <q-icon
                  v-if="selectedTask.status === 'open'"
                  size="1.8em"
                  name="edit"
                  color="primary"
                  @click="
                    () => {
                      isEditing = true
                      info_dialog = false
                      editTask(
                        selectedTask.title,
                        selectedTask.description,
                        selectedTask.start,
                        selectedTask.time,
                        selectedTask.minor || selectedTask.adult,
                        selectedTask.minor ||
                          selectedTask.guest ||
                          selectedTask.adult
                          ? false
                          : true
                      )
                    }
                  " />
                <q-icon
                  v-if="isAdmin"
                  class="q-ml-sm"
                  size="1.8em"
                  name="delete"
                  style="color: #f63333db"
                  @click="
                    askConfirm(
                      'Sei sicuro di voler eliminare la consegna?',
                      deleteTask
                    )
                  " />
              </div>
            </div>
          </q-card-section>
          <q-card-section class="q-pt-none">
            <div style="max-width: 350px">
              <q-list>
                <q-item>
                  <q-item-section>
                    <q-item-label>Consegna</q-item-label>
                    <q-item-label caption lines="2">{{
                      selectedTask.title
                    }}</q-item-label>
                  </q-item-section>
                </q-item>

                <q-separator spaced inset />

                <q-item>
                  <q-item-section>
                    <q-item-label>Descrizione</q-item-label>
                    <q-item-label caption>{{
                      selectedTask.description
                    }}</q-item-label>
                  </q-item-section>
                </q-item>
                <div
                  v-if="
                    ('minor' in selectedTask &&
                      typeof selectedTask.minor === 'object' &&
                      selectedTask.minor?.name) ||
                    ('adult' in selectedTask &&
                      typeof selectedTask.adult === 'object' &&
                      selectedTask.adult?.name)
                  ">
                  <q-separator spaced inset />

                  <q-item>
                    <q-item-section>
                      <q-item-label>Ospite</q-item-label>
                      <q-item-label
                        v-if="
                          (typeof selectedTask.minor === 'object' &&
                            selectedTask.minor?.name) ||
                          (typeof selectedTask.adult === 'object' &&
                            selectedTask.adult?.name)
                        "
                        caption
                        >{{
                          selectedTask.minor?.name
                            ? selectedTask.minor.name +
                              ' ' +
                              selectedTask.minor.surname
                            : selectedTask.adult.name +
                              ' ' +
                              selectedTask.adult.surname
                        }}</q-item-label
                      >
                    </q-item-section>
                  </q-item>
                </div>

                <q-separator spaced inset />
                <q-item>
                  <q-item-section>
                    <q-item-label>Orario consegna</q-item-label>
                    <q-item-label caption>{{ selectedTask.time }}</q-item-label>
                  </q-item-section>
                </q-item>
                <q-separator spaced inset />
                <q-item>
                  <q-item-section>
                    <q-item-label
                      >Status :
                      <q-badge
                        rounded
                        :color="eventStates[selectedTask.status].color"
                        :label="eventStates[selectedTask.status].label" />
                    </q-item-label>
                  </q-item-section>
                </q-item>
                <div v-if="'operator' in selectedTask">
                  <q-separator spaced inset />

                  <q-item>
                    <q-item-section>
                      <q-item-label>Operatore </q-item-label>
                      <q-item-label caption>{{
                        typeof selectedTask.operator === 'string'
                          ? selectedTask.operator
                          : selectedTask.operator?.name
                          ? selectedTask.operator.name +
                            ' ' +
                            selectedTask.operator.surname
                          : selectedTask.operator.companyName
                      }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </div>
              </q-list>
            </div>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn
              v-if="!isAdmin && selectedTask.status === 'open'"
              flat
              label="Prendi in carico"
              color="primary"
              @click="
                () => {
                  toggleCharge(selectedTask)
                }
              " />
            <q-btn
              v-if="
                !isAdmin &&
                selectedTask.status === 'charged' &&
                selectedTask.operator._id.$oid === operator
              "
              flat
              label="Lascia"
              color="primary"
              @click="
                () => {
                  toggleCharge(selectedTask)
                }
              " />
            <q-btn
              v-close-popup
              label="Chiudi"
              color="primary"
              @click="info_dialog = false" />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>

    <FullCalendar ref="fullCalendar" :options="calendarOptions">
      <template #eventContent="arg">
        <div class="row">
          <div>
            {{
              (typeof arg.event.extendedProps.minor === 'object' &&
              arg.event.extendedProps.minor?.name
                ? arg.event.extendedProps.minor.surname.substring(0, 1) +
                  '.' +
                  arg.event.extendedProps.minor.name
                : '') ||
              (typeof arg.event.extendedProps.adult === 'object' &&
              arg.event.extendedProps.adult?.name
                ? arg.event.extendedProps.adult.surname.substring(0, 1) +
                  '.' +
                  arg.event.extendedProps.adult.name
                : '')
            }}

            <span v-if="arg.event.title" style="display: block">
              {{ arg.event.title }}</span
            >
            <span v-else>
              <i>{{ arg.event.extendedProps.description }}</i>
            </span>
          </div>
        </div>
      </template>
    </FullCalendar>
    <q-dialog v-model="dialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">
            {{ isEditing ? 'Modifica Consegna' : 'Aggiungi Consegna' }}
          </div>
        </q-card-section>
        <q-card-section>
          <q-btn-group>
            <q-btn
              v-model="isGeneral"
              class="segmented"
              label="Consegna generale"
              :color="isGeneral ? 'primary' : undefined"
              @click="switchConsegna(true)" />
            <q-btn
              v-model="isGeneral"
              class="segmented"
              label="Consegna personale"
              :color="!isGeneral ? 'primary' : undefined"
              @click="switchConsegna(false)" />
          </q-btn-group>
        </q-card-section>
        <q-card-section class="q-pt-none">
          <form>
            <q-select
              v-if="!isGeneral"
              v-model="event['guest']"
              outlined
              :options="guests"
              label="Ospite"
              :option-label="opt => opt.name + ' ' + opt.surname">
              <template #no-option>
                <q-item>
                  <q-item-section class="text-italic text-grey">
                    Non sono presenti ospiti
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
            <!-- This is commented out because the modulo is not needed anymore -->
            <!-- <q-select
              v-else
              v-model="event.resource.module"
              outlined
              :options="hccps"
              label="Modulo"
              class="q-my-md"
              @update:model-value="getResources($event)" /> 
            <q-select
              v-if="
                'resource' in event &&
                'module' in event.resource &&
                event.resource.module !== null &&
                isHCCP &&
                hccps_resources.length > 0
              "
              v-model="event.resource.type"
              outlined
              :options="hccps_resources"
              label="Tipo"
              class="q-my-md" /> -->
            <q-input
              v-model="event.title"
              outlined
              label="Titolo"
              class="q-my-sm" />
            <q-input
              v-model="event.description"
              outlined
              label="Descrizione"
              type="textarea"
              class="q-my-md" />
            <q-input
              v-model="event.date"
              outlined
              label="Inserisci data: "
              mask="##/##/####">
              <template #append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy
                    ref="qDateProxy"
                    cover
                    transition-show="scale"
                    transition-hide="scale">
                    <q-date
                      v-model="event.date"
                      :locale="locale"
                      type="date"
                      mask="DD/MM/YYYY"
                      :options="optionsFn">
                      <div class="row items-center justify-end">
                        <q-btn
                          v-close-popup
                          label="Close"
                          color="primary"
                          flat />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
            <q-input
              v-model="event.time"
              outlined
              mask="time"
              :rules="['time']"
              class="q-mt-sm"
              label="Inserisci orario: ">
              <template #append>
                <q-icon name="access_time" class="cursor-pointer">
                  <q-popup-proxy
                    cover
                    transition-show="scale"
                    transition-hide="scale">
                    <q-time v-model="event.time" format24h>
                      <div class="row items-center justify-end">
                        <q-btn
                          v-close-popup
                          label="Close"
                          color="primary"
                          flat />
                      </div>
                    </q-time>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn v-close-popup flat label="Chiudi" color="primary" />
          <q-btn
            :label="isEditing ? 'Modifica' : 'Aggiungi'"
            color="primary"
            @click="isEditing ? editEvent() : addEvent()" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { defineComponent, watchEffect } from 'vue'
import '@fullcalendar/core/vdom' // solves problem with Vite
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import itLocale from '@fullcalendar/core/locales/it'
import { api } from 'src/boot/axios'
import { is, useQuasar } from 'quasar'
import Heading from 'components/Heading.vue'
import moment from 'moment'
import { date } from 'quasar'
import { itLocaleQDate } from 'src/const/QDateItLocale'

export default defineComponent({
  name: 'Tasks',
  components: {
    FullCalendar,
    Heading
  },
  setup() {
    const $q = useQuasar()

    return {
      optionsFn(d) {
        return d >= date.formatDate(Date.now(), 'YYYY/MM/DD')
      },
      showNotif(tp, msg) {
        $q.notify({
          type: tp,
          message: msg,
          position: 'top-right',
          timeout: 1000
        })
      }
    }
  },
  data() {
    return {
      isEditing: false,
      selectedTask: {},
      shift: '',
      operator: '',
      isAdmin: false,
      dialog: false,
      calendarOptions: {
        nextDayThreshold: '00:00:00',
        timeZone: 'UTC',
        handleWindowResize: true,
        height: 710,
        customButtons: {
          add: {
            text: 'Aggiungi',
            click: this.openDialogForCreate.bind()
          }
        },
        headerToolbar: {
          right: 'dayGridMonth,dayGridWeek today prev,next add'
        },
        locale: itLocale,
        plugins: [dayGridPlugin],
        initialView: this.isAdmin ? 'dayGridMonth' : 'dayGridWeek',
        dayMaxEvents: true,
        views: {
          dayGridMonth: {
            dayMaxEvents: 4,
            type: 'dayGridMonth'
          },
          dayGridWeek: {
            dayMaxEvents: 14,
            type: 'timeGrid',
            duration: { days: 7 },
            buttonText: 'Settimana'
          }
        },
        events: this.fetchEvents.bind(this),
        eventClick: this.onEventClick.bind(this),
        eventClassNames: function (arg) {
          return [arg.event.extendedProps.status]
        }
      },
      event: {
        guest: '',
        date: '',
        time: '',
        title: '',
        description: ''
      },
      locale: itLocaleQDate,
      isGeneral: true,
      guests: [],
      hccps: [],
      hccps_resources: [],
      search_date: null,
      info_dialog: false,
      eventStates: {
        open: { label: 'Da svolgere', color: 'blue' },
        charged: { label: 'Presa in carico', color: 'orange' },
        done: { label: 'Svolta', color: 'green' }
      }
    }
  },
  watch: {
    search_date: async function (t) {
      if (t) {
        return await t
      } else {
        return await new Date()
      }
    }
  },
  mounted() {
    this.operator = JSON.parse(sessionStorage.getItem('user')).uid
    const usertype = JSON.parse(sessionStorage.getItem('user')).usertype
    this.isAdmin = usertype === 'admin' || usertype === 'superadmin'
    this.getShift()
  },
  methods: {
    editTask(title, description, date, time, guest, isGeneral) {
      this.event = {
        title,
        description,
        date: moment(date).format('DD/MM/YYYY'),
        time,
        guest
      }
      this.isGeneral = isGeneral
      this.isEditing = true
      this.getDialogData()
      this.dialog = true
    },
    getDialogData() {
      const areGuestsLoaded = this.guests.length !== 0
      !areGuestsLoaded &&
        this.guests.length == 0 &&
        api.get('/minors/minor/all').then(response => {
          this.guests = this.guests.concat(
            response.data.map(minor => {
              return {
                ...minor,
                isMinor: true
              }
            })
          )
        })
      !areGuestsLoaded &&
        api.get('/adults/adult/all').then(response => {
          this.guests = this.guests.concat(
            response.data.map(adult => {
              return {
                ...adult,
                isMinor: false
              }
            })
          )
        })
    },
    askConfirm(message, toExecute, ...args) {
      this.$q
        .dialog({
          title: 'Conferma',
          message: message || 'Sei sicuro di voler procedere',
          cancel: 'Annulla',
          persistent: true
        })
        .onOk(() => {
          toExecute(...args)
        })
    },
    getResources(e) {
      this.event.resource.type = null
      this.hccps_resources = this.hccps.find(x => x._id === e._id).modules
    },
    containsTask(obj, list) {
      const isInArray = list.filter(function (e) {
        return e._id.$oid === obj._id.$oid
      })
      return isInArray.length > 0 ? true : false
    },
    toggleCharge(task) {
      const request = {}
      task.status === 'open'
        ? (request['charge'] = [task._id.$oid])
        : (request['discharge'] = [task._id.$oid])

      api
        .post('/tasks/task/charge', request)
        .then(response => {
          this.showNotif(
            'positive',
            `La consegna è stata ${
              task.status === 'open' ? 'presa in carico' : 'lasciata'
            } correttamente.`
          )
          this.info_dialog = false
          const calendarApi = this.$refs.fullCalendar.getApi()
          calendarApi.refetchEvents()

          api.post('/auth/log', {
            name:
              task.status === 'open' ? 'Presa in carico' : 'Consegna lasciata',
            description: `Consegna ${task.title} ${
              task.status === 'open' ? 'presa in carico' : 'lasciata'
            }`
          })
        })
        .catch(err => {
          this.showNotif(
            'warning',
            'Impossibile modificare lo stato della consegna'
          )
        })
    },
    checkDay(event) {
      const today = new Date().getDay()
      return new Date(event.view.currentStart).getDay() === today
    },
    formatTask(task) {
      const task_to_insert = {
        title: task.title,
        start: task.startStr
      }
      Object.assign(task_to_insert, task.extendedProps)
      if (task.end) {
        task_to_insert['end'] = task.endStr
      }
      return task_to_insert
    },
    getShift() {
      const now = new Date().getHours()
      if (now >= 0 && now <= 14) {
        this.shift = 'Mattina'
      } else if (now > 14 && now <= 18) {
        this.shift = 'Pomeriggio'
      } else {
        this.shift = 'Sera'
      }
    },
    openDialogForCreate() {
      this.event = {
        title: '',
        description: '',
        start: ''
      }
      this.isEditing = false
      this.getDialogData()
      this.dialog = true
      this.isGeneral = true
    },
    switchConsegna(e) {
      if (e) {
        this.isGeneral = true
        delete this.event['guest']
      } else {
        this.isGeneral = false
        this.event['guest'] = null
      }
    },
    watchDate(value, reason, detail) {
      this.event.date = moment(value).format('DD/MM/YYYY')
    },
    deleteTask() {
      api
        .delete('/tasks/task/' + this.selectedTask._id.$oid)
        .then(response => {
          this.showNotif(
            'positive',
            'La consegna è stata eliminata correttamente.'
          )
          this.info_dialog = false
          const calendarApi = this.$refs.fullCalendar.getApi()
          calendarApi.refetchEvents()
        })
        .catch(er => {
          this.showNotif('negative', 'Impossibile eliminare la consegna')
        })
    },
    validate() {
      let isValid = true
      // this code is commented out because the module is not used anymore
      // if (
      //   this.isHCCP &&
      //   (Object.keys(this.event.resource) === 0 ||
      //     this.event.resource.module === '')
      // ) {
      //   isValid = false
      //   this.showNotif('warning', 'Il campo Modulo HCCP deve essere inserito.')
      // }
      if (!this.isGeneral && !this.event.guest) {
        isValid = false
        this.showNotif('warning', 'Il campo Ospite deve essere inserito.')
      }
      if (!this.event?.date) {
        isValid = false
        this.showNotif('warning', 'Il campo Data deve essere inserito.')
      }
      if (!this.event?.time) {
        isValid = false
        this.showNotif('warning', 'Il campo Ora deve essere inserito.')
      }
      if (this.event.title === '' || this.event.title.trim() === '') {
        isValid = false
        this.showNotif('warning', 'Il campo Titolo deve essere inserito.')
      }
      this.formatTitle(this.event.title)

      return isValid
    },
    formatTitle(title) {
      const str = title.toLowerCase()
      const toCapitalize = str.charAt(0).toUpperCase()
      this.event.title = toCapitalize + '' + str.slice(1)
    },
    editEvent() {
      if (this.validate()) {
        this.event['start'] = this.event.date + ' ' + this.event.time
        delete this.event['date']
        delete this.event['time']
        this.dialog = false
        const result = this.event
        const guest = result.guest
        result.minor = guest && guest.isMinor ? guest._id.$oid : undefined
        result.adult = guest && !guest.isMinor ? guest._id.$oid : undefined
        result.isGeneral = this.isGeneral ? 'True' : 'False'
        //don't remove this line, the backend needs the resource field
        result.resource = {
          module: null,
          type: null
        }
        api
          .put('/tasks/task/' + this.selectedTask._id.$oid, result)
          .then(resp => {
            this.showNotif(
              'positive',
              'La consegna è stata modificata correttamente!'
            )
            const calendarApi = this.$refs.fullCalendar.getApi()
            calendarApi.refetchEvents()
          })
          .catch(err => {
            this.showNotif('negative', 'Impossibile modificare la consegna!')
          })
      }
    },
    addEvent() {
      if (this.validate()) {
        this.event['start'] = this.event.date + ' ' + this.event.time
        delete this.event['date']
        delete this.event['time']
        this.dialog = false
        const result = this.event
        const guest = result.guest
        result.minor = guest && guest.isMinor ? guest._id.$oid : undefined
        result.adult = guest && !guest.isMinor ? guest._id.$oid : undefined
        //don't remove this line, the backend needs the resource field
        result.resource = {
          module: null,
          type: null
        }
        api
          .post('/tasks/task', result)
          .then(resp => {
            this.showNotif(
              'positive',
              'La consegna è stata aggiunta correttamente!'
            )
            const calendarApi = this.$refs.fullCalendar.getApi()
            calendarApi.refetchEvents()
          })
          .catch(err => {
            this.showNotif('negative', 'Impossibile aggiungere la consegna!')
          })
      }
    },
    fetchEvents: async function (t) {
      try {
        const response = await api.get('/tasks/task', {
          params: { startdate: t.start, enddate: t.end }
        })
        return response.data.map(event => {
          return {
            ...event,
            allDay: true,
            time: new Date(event.start).toLocaleTimeString('it-IT', {
              hour: '2-digit',
              minute: '2-digit'
            })
          }
        })
      } catch (exception) {
        // storing my error onto Sentry
      }
      return []
    },
    onEventClick: async function (info) {
      const eventObj = {
        start: info.event.startStr,
        title: info.event.title
      }
      this.selectedTask = Object.assign(eventObj, info.event.extendedProps)
      this.info_dialog = true
    }
  }
})
</script>

<style scoped>
.fc.fc-media-screen.fc-direction-ltr.fc-theme-standard.fc-liquid-hack {
  width: 80%;
  margin-left: 10%;
  margin-top: 5%;
  margin-bottom: 5%;
}

.col-1 {
  display: flex;
  justify-content: end;
}

.fc .fc-toolbar-title {
  font-size: 1.6em;
}

.fc-scroller.fc-scroller-liquid-absolute {
  overflow: visible;
}
</style>
<style>
h5 {
  margin-top: 20px;
  margin-bottom: 30px;
}

/*events background*/
a.fc-daygrid-event.charged,
a.fc-daygrid-event.charged,
a.fc-daygrid-event.charged {
  background: #ffc458d6;
}

a.fc-daygrid-event.done,
a.fc-daygrid-event.done,
a.fc-daygrid-event.done {
  background: #7cff7ce8;
}

a.fc-daygrid-event.open,
a.fc-daygrid-event.open,
a.fc-daygrid-event.open {
  background: #76a9ff6e;
}

.fc-daygrid-event {
  padding: 5px !important;
}
.fc-h-event .fc-event-main {
  color: #000 !important;
}
@media (min-width: 600px) {
  .q-dialog__inner--minimized > div {
    min-width: 306px;
  }
}

.fc-daygrid-event-harness {
  overflow: hidden;
  margin-top: 4px !important;
}

.q-dialog.fullscreen.no-pointer-events.q-dialog--modal {
  z-index: 10000;
}

.q-menu.q-position-engine.scroll,
.q-notifications__list.q-notifications__list--top.fixed.column.no-wrap.items-end {
  z-index: 11000;
}

span.fc-icon.fc-icon-chevron-left::before {
  font-family: 'Font Awesome 5 Free';
  content: '\f053';
  font-weight: 800;
}

span.fc-icon.fc-icon-chevron-right::before {
  content: '\f054';
  font-family: 'Font Awesome 5 Free';
  font-weight: 800;
}

.fc.fc-media-screen.fc-direction-ltr.fc-theme-standard {
  background: white;
  box-shadow: 0 1px 5px rgb(0 0 0 / 20%), 0 2px 2px rgb(0 0 0 / 14%),
    0 3px 1px -2px rgb(0 0 0 / 12%);
  border-radius: 4px;
  padding-left: 10px;
  padding-right: 10px;
}

.segmented {
  padding: 15px;
}

.fc-button-active {
  background-color: #567a9f !important;
}
</style>
