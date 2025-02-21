<template>
  <q-page class="q-mb-md q-mx-xl">
    <div class="row" style="height: 60px"></div>

    <div style="display: flex; align-items: center">
      <q-dialog v-model="info_dialog">
        <q-card style="min-width: 350px">
          <q-card-section>
            <div class="row">
              <div class="col-11">
                <div class="text-h6">Dettagli turno</div>
              </div>
              <div class="col-1">
                <q-icon
                  size="1.8em"
                  name="delete"
                  style="color: #f63333db"
                  @click="
                    askConfirm(
                      'Sei sicuro di voler eliminare il turno?',
                      deleteEvent
                    )
                  " />
              </div>
            </div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-list>
              <q-item>
                <q-item-section>
                  <q-item-label>Operatore</q-item-label>
                  <q-item-label caption>{{ selectedEvent.title }}</q-item-label>
                </q-item-section>
              </q-item>

              <q-separator spaced inset />

              <q-item>
                <q-item-section>
                  <q-item-label>Durata turno</q-item-label>
                  <q-item-label caption
                    >{{ selectedEvent.duration }} ore</q-item-label
                  >
                </q-item-section>
              </q-item>

              <q-separator spaced inset />

              <q-item>
                <q-item-section>
                  <q-item-label>Costo orario</q-item-label>
                  <q-item-label caption
                    >€ {{ selectedEvent.operatorHourlyCost }}</q-item-label
                  >
                </q-item-section>
              </q-item>

              <q-separator spaced inset />

              <q-item>
                <q-item-section>
                  <q-item-label>Data</q-item-label>
                  <q-item-label caption>{{
                    formatDate(selectedEvent.start)
                  }}</q-item-label>
                </q-item-section>
              </q-item>

              <q-separator spaced inset />

              <q-item>
                <q-item-section>
                  <q-item-label>Ora inizio</q-item-label>
                  <q-item-label caption>{{
                    selectedEvent.extendedProps.startTime
                  }}</q-item-label>
                </q-item-section>
              </q-item>

              <q-separator spaced inset />

              <q-item>
                <q-item-section>
                  <q-item-label>Ora fine</q-item-label>
                  <q-item-label caption>{{
                    selectedEvent.extendedProps.endTime
                  }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn
              v-close-popup
              flat
              label="Chiudi"
              color="primary"
              @click="info_dialog = false" />
            <q-btn label="Modifica" color="primary" @click="editShift" />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
    <div class="scheduler-container">
      <div class="operators-sidebar">
        <q-list>
          <q-item-label header class="operators-header">
            List of Operators
            <q-btn
              flat
              round
              icon="file_download"
              color="primary"
              :loading="false"
              data-csv-download
              class="float-right"
              size="sm"
              title="Download as CSV"
              @click="downloadOperatorsCSV" />
          </q-item-label>
          <q-item
            v-for="operatori in operators"
            :key="operatori.id"
            v-ripple
            class="operator-list-item"
            clickable>
            <q-checkbox
              v-model="operatori.selected"
              :color="operatori.color"
              @update:model-value="updateCalendar"></q-checkbox>
            <q-item-section>{{ operatori.name }}</q-item-section>
            <q-item-section side center>€{{ operatori.price }}</q-item-section>
          </q-item>
        </q-list>
        <div
          v-if="existingExtraCosts.length > 0"
          class="existing-extra-costs-section">
          <h6 class="section-title">Extra Costs</h6>
          <div
            v-for="(cost, index) in existingExtraCosts"
            :key="index"
            class="existing-extra-cost-item q-mb-xs">
            <span class="cost-title">{{ cost.title }}</span>
            <span class="cost-amount">€{{ cost.amount.toFixed(2) }}</span>
            <q-btn
              flat
              dense
              round
              icon="close"
              color="negative"
              @click="deleteExtraCost(cost)" />
          </div>
        </div>
        <div class="q-mb-md extra-costs-section">
          <div class="button-row justify-beteween q-mt-md">
            <q-btn color="primary" @click="addExtraCost">
              <q-icon name="add" class="on-left" />
              ADD
            </q-btn>
            <q-btn color="positive" @click="saveExtraCosts">
              <q-icon name="save" class="on-left" />
              SAVE
            </q-btn>
          </div>

          <div
            v-for="(cost, index) in extraCosts"
            :key="index"
            class="row q-col-gutter-sm q-mb-sm items-center">
            <div class="col-5">
              <q-input v-model="cost.title" label="Title" dense />
            </div>
            <div class="col-5">
              <q-input
                v-model.number="cost.amount"
                label="Amount"
                type="number"
                dense
                prefix="€" />
            </div>
            <div class="col-2">
              <q-btn
                flat
                dense
                round
                icon="close"
                color="negative"
                @click="removeExtraCost(index)" />
            </div>
          </div>
        </div>

        <div class="total-price">
          Total:
          <div>€{{ totalCost.toFixed(2) }}</div>
        </div>
      </div>

      <div class="calendar-container">
        <FullCalendar ref="fullCalendar" :options="calendarOptions">
          <template #eventContent="arg">
            <div class="event-content">
              <span
                class="operator-color-dot"
                :style="{
                  backgroundColor: getOperatorColor(
                    arg.event.extendedProps.operatorId
                  )
                }"></span>
              <span class="operator-name">{{ arg.event.title }}</span>
            </div>
          </template>
        </FullCalendar>
      </div>
    </div>
    <q-dialog v-model="dialog" @hide="closeDialog" @close="closeDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Aggiungi turno</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <form>
            <q-select
              v-model="newShift.operator"
              :options="operators"
              option-label="name"
              option-value="id"
              outlined
              label="Operatore"
              class="q-mb-md" />

            <q-input
              v-model="newShift.date"
              outlined
              label="Inserisci data: "
              mask="####/##/##"
              readonly>
              <template #append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy
                    ref="qDateProxy"
                    cover
                    transition-show="scale"
                    transition-hide="scale">
                    <q-date
                      v-model="newShift.date"
                      :options="optionsFn"
                      @update:model-value="
                        (value, reason, detail) => {
                          watchDate(value, reason, detail)
                        }
                      ">
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
              v-model="newShift.startTime"
              outlined
              mask="time"
              :rules="['time']"
              class="q-mt-sm"
              label="Inserisci ora inizio: "
              readonly>
              <template #append>
                <q-icon name="access_time" class="cursor-pointer">
                  <q-popup-proxy
                    cover
                    transition-show="scale"
                    transition-hide="scale">
                    <q-time v-model="newShift.startTime" format24h>
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

            <q-input
              v-model="newShift.endTime"
              outlined
              mask="time"
              :rules="['time']"
              class="q-mt-sm"
              label="Inserisci ora fine: "
              readonly>
              <template #append>
                <q-icon name="access_time" class="cursor-pointer">
                  <q-popup-proxy
                    cover
                    transition-show="scale"
                    transition-hide="scale">
                    <q-time v-model="newShift.endTime" format24h>
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
          <q-btn
            v-close-popup
            flat
            label="Chiudi"
            color="primary"
            @click="closeDialog" />
          <q-btn
            v-if="!isEditing"
            label="Aggiungi"
            color="primary"
            @click="addShift" />
          <q-btn v-else label="Aggiorna" color="primary" @click="updateShift" />
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
import { useQuasar } from 'quasar'
import moment from 'moment'
import { date } from 'quasar'

export default defineComponent({
  name: 'Scheduler',
  components: {
    FullCalendar
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
      totalCost: 0,
      selectedDate: '',
      extraCosts: [],
      existingExtraCosts: [],
      showSave: false,
      selectedEvents: [],
      unselectedEvents: [],
      selectedEvent: {},
      shifts: '',
      operator: '',
      dialog: false,
      newShift: {
        operator: null,
        date: '',
        startTime: '',
        endTime: ''
      },
      isEditing: false,
      operators: [],
      calendarOptions: {
        timeZone: 'UTC',
        handleWindowResize: true,
        height: 710,
        customButtons: {
          takeCharge: {
            text: 'Aggiungi',
            click: this.openDialog.bind()
          }
        },
        headerToolbar: {
          right: 'today prev,next takeCharge'
        },
        locale: itLocale,
        plugins: [dayGridPlugin],
        initialView: 'dayGridMonth',
        dayMaxEvents: false, // Allow showing all events
        eventDisplay: 'block', // Display events as blocks
        datesSet: this.handleDatesSet,
        events: this.fetchShifts.bind(this),
        //shifts: this.fetchShifts.bind(this), // TODO: Rewrite the fetch shifts according to the shifts
        eventClick: this.onEventClick.bind(this),
        eventClassNames: function (arg) {
          return [arg.event.extendedProps.status]
        }
      },
      event: {
        minor: null,
        date: '',
        time: '',
        title: '',
        description: '',
        status: ''
      },
      minors: [],
      search_date: null,
      info_dialog: false,
      urgency: [
        {
          label: 'Normale',
          value: 'normal'
        },
        {
          label: 'Urgente',
          value: 'urgent'
        }
      ],
      eventStates: {
        normal: { label: 'Normale', color: 'green' },
        urgent: { label: 'Urgente', color: 'red' }
      }
    }
  },
  computed: {
    totalPrice() {
      return this.operators
        .filter(o => o.selected)
        .reduce((sum, operator) => sum + operator.price, 0)
        .toFixed(2)
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
    this.fetchOperators().then(() => {
      const calendarApi = this.$refs.fullCalendar.getApi()
      calendarApi.refetchEvents()
    })
    this.getShifts()
  },
  methods: {
    getYearAndMonth(d) {
      if (!d) {
        const date = new Date(this.selectedDate)
        return {
          year: date.getUTCFullYear(),
          month: date.getUTCMonth() + 1 // JavaScript months are 0-indexed
        }
      }
      const date = new Date(d)
      return {
        year: date.getUTCFullYear(),
        month: date.getUTCMonth() + 1 // JavaScript months are 0-indexed
      }
    },
    addExtraCost() {
      this.extraCosts.push({ title: '', amount: 0 })
      this.showSave = true
    },
    deleteExtraCost: async function (cost) {
      try {
        const { year, month } = this.getYearAndMonth()
        const response = await api.delete('/extra-costs', {
          data: {
            year,
            month,
            item_name: cost.title,
            cost: cost.amount
          }
        })
        console.log('response is', response)
        if (response.data.success) {
          this.existingExtraCosts = this.existingExtraCosts.filter(
            c => !(c.title === cost.title && c.amount === cost.amount)
          )
          this.totalCost -= cost.amount
          this.showNotif('positive', 'Extra cost deleted successfully')
        } else {
          this.showNotif('negative', 'Failed to delete extra cost')
        }
      } catch (error) {
        console.error('Error deleting extra cost:', error)
        this.showNotif('negative', 'Error deleting extra cost')
      }
    },
    saveExtraCosts: async function () {
      try {
        const { year, month } = this.getYearAndMonth()
        console.log('Extra costs to save:', this.extraCosts)
        console.log({ year, month })
        for (const cost of this.extraCosts) {
          await api.post('/extra-costs', {
            year,
            month,
            item_name: cost.title,
            cost: parseFloat(cost.amount)
          })
        }

        this.showNotif('positive', 'Extra costs saved successfully')
        this.showSave = false
        this.extraCosts = [] // Clear the list after successful save

        // Optionally, refresh the total price or other relevant data
        this.updateCalendar()
      } catch (error) {
        console.error('Error saving extra costs:', error)
        this.showNotif(
          'negative',
          'Failed to save extra costs. Please try again.'
        )
      }
    },
    fetchExtraCosts: async function (date) {
      try {
        const { year, month } = this.getYearAndMonth(date)
        const response = await api.get('/extra-costs', {
          params: { year, month }
        })

        // Process the fetched extra costs
        this.existingExtraCosts = response.data.extra_costs.map(cost => ({
          title: cost.item_name,
          amount: cost.cost
        }))

        this.totalCost = response.data.total_cost

        // If there are fetched costs, show the save button
        this.showSave = this.existingExtraCosts.length > 0

        console.log('Fetched extra costs:', response.data)
      } catch (error) {
        console.error('Error fetching extra costs:', error)
        this.showNotif('negative', 'Failed to fetch extra costs.')
      }
    },
    removeExtraCost(index) {
      this.extraCosts.splice(index, 1)
      if (this.extraCosts.length === 0) {
        this.showSave = false
      }
    },
    getShifts() {
      const now = new Date().getHours()
      if (now >= 0 && now <= 14) {
        this.shift = 'Mattina'
      } else if (now > 14 && now <= 18) {
        this.shift = 'Pomeriggio'
      } else {
        this.shift = 'Sera'
      }
    },
    openDialog() {
      this.newShift = {
        operator: null,
        date: '',
        startTime: '',
        endTime: ''
      }
      this.dialog = true
    },

    addShift() {
      if (this.validateShift()) {
        // Format the shift data as needed for your API
        const shiftData = {
          operatorId: this.newShift.operator.id,
          date: this.event.date,
          startTime: this.newShift.startTime,
          endTime: this.newShift.endTime
        }

        // Call your API to add the shift
        api
          .post('/shifts', shiftData)
          .then(response => {
            this.showNotif('positive', 'Turno aggiunto con successo')
            this.dialog = false
            const calendarApi = this.$refs.fullCalendar.getApi()
            calendarApi.refetchEvents()
            // Refresh your calendar or shift list here
          })
          .catch(error => {
            this.showNotif('negative', "Errore nell'aggiunta del turno")
            console.error('Error adding shift:', error)
          })
      }
    },
    editShift() {
      let dateToFormat = this.selectedEvent.extendedProps.date
      // If it's already a Date object, convert it to an ISO string
      if (dateToFormat instanceof Date) {
        dateToFormat = dateToFormat.toISOString()
      }

      // Now use moment to format the date
      const formattedDate = moment(dateToFormat, 'DD/MM/YYYY').format(
        'YYYY/MM/DD'
      )
      this.newShift = {
        operator: this.operators.find(
          op => op.id === this.selectedEvent.extendedProps.operatorId
        ),
        date: formattedDate,
        startTime: this.formatTimeForInput(
          this.selectedEvent.extendedProps.startTime
        ),
        endTime: this.formatTimeForInput(
          this.selectedEvent.extendedProps.endTime
        )
      }
      this.event.date = formattedDate
      this.isEditing = true
      this.info_dialog = false
      this.dialog = true
    },
    onDateSelect(value) {
      this.newShift.date = this.formatDate(value)
      this.$refs.qDateProxy.hide()
    },
    isOperatorSelected(operatorId) {
      const opr = this.operators.find(op => op.id === operatorId)
      return opr && opr.selected
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      const day = date.getDate().toString().padStart(2, '0')
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const year = date.getFullYear()
      return `${day}/${month}/${year}`
    },

    formatTimeForInput(date) {
      return date.toTimeString().slice(0, 5) // This will return "HH:mm"
    },

    handleDatesSet(dateInfo) {
      const calendarApi = this.$refs.fullCalendar.getApi()
      calendarApi.refetchEvents()
    },
    validateShift() {
      if (!this.newShift.operator) {
        this.showNotif('warning', 'Seleziona un operatore')
        return false
      }
      if (!this.newShift.date) {
        this.showNotif('warning', 'Inserisci una data')
        return false
      }
      if (!this.newShift.startTime) {
        this.showNotif('warning', "Inserisci l'ora di inizio")
        return false
      }
      if (!this.newShift.endTime) {
        this.showNotif('warning', "Inserisci l'ora di fine")
        return false
      }
      return true
    },
    watchDate(value, reason, detail) {
      this.event.date = moment(value).format('DD/MM/YYYY')
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
    deleteEvent() {
      api
        .delete('/shifts/' + this.selectedEvent.id)
        .then(response => {
          this.showNotif(
            'positive',
            'La mansione è stata eliminata correttamente.'
          )
          this.info_dialog = false
          const calendarApi = this.$refs.fullCalendar.getApi()
          calendarApi.refetchEvents()
        })
        .catch(er => {
          this.showNotif('negative', 'Impossibile eliminare la mansione')
        })
    },
    validate() {
      let isValid = true
      if (!this.event?.date) {
        isValid = false
        this.showNotif('warning', 'Il campo Data deve essere inserito.')
      }
      if (!this.event?.time) {
        isValid = false
        this.showNotif('warning', 'Il campo Ora deve essere inserito.')
      }
      this.formatTitle(this.event.title)

      return isValid
    },
    formatTitle(title) {
      const str = title.toLowerCase()
      const toCapitalize = str.charAt(0).toUpperCase()
      this.event.title = toCapitalize + '' + str.slice(1)
    },
    getRandomColor() {
      const colors = [
        'teal',
        'orange',
        'red',
        'cyan',
        'purple',
        'green',
        'blue',
        'magenta',
        'yellow',
        'black'
      ]
      const randomIndex = Math.floor(Math.random() * colors.length)
      const selectedColor = colors[randomIndex]
      return selectedColor
    },
    getOperatorColor(operatorId) {
      const operator = this.operators.find(op => op.id == operatorId)
      return operator ? operator.color : '#000000' // Default to black if not found
    },
    updateCalendar() {
      if (this.$refs.fullCalendar) {
        const calendarApi = this.$refs.fullCalendar.getApi()
        calendarApi.refetchEvents()
      }
    },
    updateOperatorsWithShiftData: function (operatorCosts) {
      // Create a Set of operator IDs from operatorCosts for faster lookup
      const costOperatorIds = new Set(
        operatorCosts.map(cost => cost.operator_id)
      )

      this.operators.forEach(operator => {
        const cost = operatorCosts.find(
          cost => cost.operator_id === operator.id
        )
        if (cost) {
          operator.hourly_cost = cost.hourly_cost
          operator.total_hours = cost.total_hours
          operator.price = cost.total_cost
        } else {
          // If the operator is not in operatorCosts, set price to 0
          operator.price = 0
          // Optionally, you might want to reset other fields as well
          operator.hourly_cost = 0
          operator.total_hours = 0
        }
      })
    },
    fetchShifts: async function (t) {
      t = t.start
      if (t.getDate() !== 1) {
        t.setDate(1)
        t.setMonth(t.getMonth() === 11 ? 0 : t.getMonth() + 1)
      }
      this.selectedDate = t
      this.fetchExtraCosts(t)
      try {
        const response = await api.get('/shifts', {
          params: { date: t }
        })
        this.updateOperatorsWithShiftData(response.data.operator_costs)
        const selectedOperatorIds = this.operators
          .filter(op => op.selected)
          .map(op => op.id)
        const tmp = response.data.shifts
          .filter(shift => selectedOperatorIds.includes(shift.operatorId.$oid))
          .map(shift => {
            const shiftDate = new Date(shift.date.$date)
            const startTime = this.parseTime(shift.startTime, shiftDate)
            const endTime = this.parseTime(shift.endTime, shiftDate)

            return {
              id: shift._id.$oid,
              title: this.getOperatorName(shift.operatorId.$oid),
              start: startTime,
              end: endTime,
              extendedProps: {
                operatorId: shift.operatorId.$oid,
                startTime: this.formatTime(startTime),
                endTime: this.formatTime(endTime),
                date: shiftDate
              }
            }
          })
        return tmp
      } catch (exception) {
        console.error('Error fetching shifts:', exception)
        // storing my error onto Sentry
      }
      return []
    },

    updateShift() {
      // Prepare the data to be sent to the API
      const updatedShiftData = {
        operatorId: this.newShift.operator.id,
        date: this.event.date,
        startTime: this.newShift.startTime,
        endTime: this.newShift.endTime
      }

      api
        .put(`/shifts/${this.selectedEvent.id}`, updatedShiftData)
        .then(() => {
          this.$q.notify({
            color: 'positive',
            message: 'Turno aggiornato con successo'
          })
          this.closeDialog()
          const calendarApi = this.$refs.fullCalendar.getApi()
          calendarApi.refetchEvents()
        })
        .catch(error => {
          console.error('Error updating shift:', error)
          this.$q.notify({
            color: 'negative',
            message: "Errore durante l'aggiornamento del turno"
          })
        })
    },

    closeDialog() {
      this.dialog = false
      this.isEditing = false
      this.newShift = {}
      this.selectedEvent = {}
    },
    parseTime(time, date) {
      if (typeof time === 'string') {
        const [hours, minutes] = time.split(':')
        return new Date(
          date.getFullYear(),
          date.getMonth(),
          date.getDate(),
          parseInt(hours),
          parseInt(minutes)
        )
      } else if (time && time.$date) {
        return new Date(time.$date)
      }
      return null
    },

    formatTime(date) {
      if (!date) return ''
      return date.toTimeString().slice(0, 5) // Returns time in "HH:MM" format
    },
    getOperatorName(operatorId) {
      const operator = this.operators.find(op => op.id === operatorId)
      return operator ? `${operator.name}` : 'Unknown'
    },
    fetchOperators: async function (t) {
      try {
        const response = await api.get('auth/user/operators', {
          params: { status: 'enabled' }
        })
        this.operators = response.data.map(operator => ({
          id: operator._id.$oid,
          name: `${operator.name} ${operator.surname}`,
          selected: true,
          price: 0,
          color: this.getRandomColor()
        }))
      } catch (error) {
        console.error('Error fetching operators:', error)
        this.showNotif('negative', 'Unable to fetch operators')
      }
    },
    onEventClick: async function (info) {
      const originalDate = new Date(info.event.extendedProps.date)
      const formattedDate = `${String(originalDate.getUTCDate()).padStart(
        2,
        '0'
      )}/${String(originalDate.getUTCMonth() + 1).padStart(
        2,
        '0'
      )}/${originalDate.getUTCFullYear()}`

      this.selectedEvent = {
        id: info.event.id,
        title: info.event.title,
        date: formattedDate, // Use the formatted date here
        start: info.event.start,
        end: info.event.extendedProps.endTime,
        extendedProps: {
          operatorId: info.event.extendedProps.operatorId,
          date: formattedDate,
          startTime: info.event.start,
          endTime: info.event.end
        }
      }

      // If you need to fetch additional details about the operator, you can do it here
      const operator = this.operators.find(
        op => op.id === this.selectedEvent.extendedProps.operatorId
      )
      if (operator) {
        this.selectedEvent.operatorName = operator.name
        this.selectedEvent.operatorHourlyCost = operator.hourly_cost
      }

      // Calculate shift duration
      const startTime = this.selectedEvent.start
      const endTime = this.selectedEvent.extendedProps.endTime
      const durationMs = endTime.getTime() - startTime.getTime()
      this.selectedEvent.duration = (durationMs / (1000 * 60 * 60)).toFixed(2) // duration in hours

      this.info_dialog = true
    },
    async downloadOperatorsCSV() {
      try {
        const btn = document.querySelector('[data-csv-download]')
        if (btn) {
          btn.classList.add('q-btn--loading')
        }

        const currentDate = {
          start: this.search_date || new Date()
        }

        if (!this.operators.some(op => op.price > 0)) {
          await this.fetchShifts(currentDate)
          await new Promise(resolve => setTimeout(resolve, 500))
        }

        if (!this.existingExtraCosts || this.existingExtraCosts.length === 0) {
          await this.fetchExtraCosts(currentDate.start)
          await new Promise(resolve => setTimeout(resolve, 500))
        }

        const totalOperatorCost = this.operators.reduce(
          (sum, op) => sum + (op.price || 0),
          0
        )
        const totalExtraCost = this.existingExtraCosts.reduce(
          (sum, cost) => sum + (parseFloat(cost.amount) || 0),
          0
        )
        const headers = ['Category', 'Description', 'Amount']
        const rows = []
        rows.push(['Operators', '', ''])
        this.operators
          .filter(op => op.name)
          .forEach(op => {
            rows.push(['', op.name, (op.price || 0).toFixed(2)])
          })
        rows.push(['', 'Total Operators', totalOperatorCost.toFixed(2)])
        rows.push(['', '', ''])

        if (this.existingExtraCosts && this.existingExtraCosts.length > 0) {
          rows.push(['Extra Costs', '', ''])
          this.existingExtraCosts.forEach(cost => {
            console.log('cost for ', cost)
            console.log('cost is', cost)
            if (cost.title && cost.amount) {
              rows.push(['', cost.title, parseFloat(cost.amount).toFixed(2)])
            }
          })
          rows.push(['', 'Total Extra Costs', totalExtraCost.toFixed(2)])
        }

        rows.push(['', '', ''])
        rows.push([
          '',
          'GRAND TOTAL',
          (totalOperatorCost + totalExtraCost).toFixed(2)
        ])

        const csvContent = [
          headers.join(','),
          ...rows.map(row => row.join(','))
        ].join('\n')

        // Create and trigger download
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
        const link = document.createElement('a')
        const url = URL.createObjectURL(blob)

        link.setAttribute('href', url)
        link.setAttribute(
          'download',
          `operators_report_${this.formatDate(currentDate.start)}.csv`
        )
        link.style.visibility = 'hidden'

        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)

        // Clean up
        URL.revokeObjectURL(url)
      } catch (error) {
        console.error('Error generating CSV:', error)
        this.$q.notify({
          color: 'negative',
          message: 'Error generating CSV file'
        })
      } finally {
        // Remove loading state
        const btn = document.querySelector('[data-csv-download]')
        if (btn) {
          btn.classList.remove('q-btn--loading')
        }
      }
    }
  }
})
</script>

<style scoped>
.justify-beteween {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.extra-costs-section,
.existing-extra-costs-section {
  margin-right: 10px;
  margin-top: 20px;
  border-radius: 4px;
}

.section-title {
  font-weight: bold;
  margin-bottom: 10px;
}

.extra-cost-item,
.existing-extra-cost-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 5px;
}

.existing-extra-cost-item {
  background-color: white;
  padding: 5px 10px;
  border-radius: 4px;
}

.cost-title {
  flex-grow: 1;
}

.cost-amount {
  margin-right: 10px;
  font-weight: bold;
}

.full-width {
  width: 100%;
}

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
.extra-costs-section {
  background-color: #f5f5f5;
  border-radius: 4px;
  padding: 16px;
}

.button-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.add-btn,
.save-btn {
  flex-grow: 1;
  margin: 0 4px;
}

@media (max-width: 600px) {
  .button-row {
    flex-direction: column;
  }

  .add-btn,
  .save-btn {
    width: 100%;
    margin: 4px 0;
  }
}

h5 {
  margin-top: 20px;
  margin-bottom: 30px;
}

/*shifts background*/
a.fc-daygrid-event.fc-daygrid-dot-event.fc-event.fc-event-start.fc-event-end.fc-event-past.urgent,
a.fc-daygrid-event.fc-daygrid-dot-event.fc-event.fc-event-start.fc-event-end.urgent,
a.fc-daygrid-event.fc-daygrid-dot-event.fc-event.fc-event-start.fc-event-end.fc-event-future.urgent {
  background: #ff5b31d6;
}

a.fc-daygrid-event.fc-daygrid-dot-event.fc-event.fc-event-start.fc-event-end.fc-event-past.normal,
a.fc-daygrid-event.fc-daygrid-dot-event.fc-event.fc-event-start.fc-event-end.normal,
a.fc-daygrid-event.fc-daygrid-dot-event.fc-event.fc-event-start.fc-event-end.fc-event-future.normal {
  background: #b6ff76c8;
}

@media (min-width: 600px) {
  .q-dialog__inner--minimized > div {
    min-width: 306px;
  }
}

.fc-daygrid-event-harness {
  overflow: hidden;
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

.scheduler-container {
  display: flex;
  width: 100%;
  /* Ensures the container takes full width of its parent */
}

.operators-sidebar {
  flex: 0 0 250px;
  /* Adjust width as needed, does not grow or shrink */
  overflow-y: auto;
  /* Adds scroll to the operators list if it exceeds the container height */
  height: calc(100vh - 20px);
  /* Adjust height based on your header/footer */
  border-right: 1px solid #ccc;
  /* Optional: adds a line between the list and the calendar */
}

.calendar-container {
  flex-grow: 1;
  /* Takes up remaining space */
  padding: 10px;
  /* Optional padding */
}

.operators-header {
  font-size: 1.5em;
  /* Larger font size */
  font-weight: bold;
  /* Bold font weight */
  padding: 10px 0;
  /* Optional padding for better spacing */
  margin-bottom: 20px;
  color: black;
}

.operator-list-item {
  padding: 10px 20px 10px 2px;
}

.total-price {
  font-size: 16px;
  font-weight: bold;
  padding: 10px;
  border-top: 1px solid #ccc;
  margin-right: 20px;
  display: flex;
  justify-content: space-between;
}

@media (max-width: 800px) {
  .scheduler-container {
    flex-direction: column;
  }

  .operators-sidebar {
    width: 100%;
    /* Full width on smaller screens */
    height: auto;
  }

  .calendar-container {
    width: 100%;
    /* Full width on smaller screens */
  }
}

.q-field--with-bottom {
  padding-bottom: 0 !important;
}
</style>

<style scoped>
.event-content {
  display: flex;
  align-items: center;
  font-size: 0.9em;
  padding: 2px 4px;
}

.operator-color-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 4px;
  display: inline-block;
}

.operator-name {
  color: black;
  font-weight: normal;
}

/* Override FullCalendar's default event styling */
:deep(.fc-event-main) {
  padding: 0;
}

:deep(.fc-event) {
  background-color: transparent;
  border: none;
}

:deep(.fc-event-title) {
  padding: 0;
}
</style>
