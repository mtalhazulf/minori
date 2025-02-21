<template>
  <q-page class="q-mb-md q-mx-xl">
    <div class="row" style="height: 60px">
      <Heading :title="'Quaderno delle Consegne'" />
    </div>
    <div style="display: flex; align-items: center"></div>
    <FullCalendar ref="fullCalendar" :options="calendarOptions">
      <template #eventContent="arg">
        <div class="row">
          <div class="col-11" @click="onEventClick(arg)">
            <b>{{
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
            }}</b>
            <span
              v-if="
                (typeof arg.event.extendedProps.minor === 'object' &&
                  arg.event.extendedProps.minor?.name) ||
                (typeof arg.event.extendedProps.adult === 'object' &&
                  arg.event.extendedProps.adult?.name)
              ">
              - </span
            ><i>{{ arg.event.title }}</i>
            {{
              arg.event.extendedProps.description !== ''
                ? ' : ' + arg.event.extendedProps.description
                : ''
            }}
          </div>
          <div v-if="checkDay(arg)" class="col-1">
            <input
              type="checkbox"
              style="width: 60%; height: 70%"
              :checked="arg.event.extendedProps.selected"
              :disabled="
                (arg.event.extendedProps.selected &&
                  arg.event.extendedProps.operator._id.$oid !== operator) ||
                arg.event.extendedProps.status === 'done'
              "
              @click="selectTask(arg.event)" />
          </div>
        </div>
      </template>
    </FullCalendar>
    <q-dialog v-model="dialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Aggiungi Consegna</div>
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
              mask="##/##/####"
              readonly>
              <template #append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy
                    ref="qDateProxy"
                    cover
                    transition-show="scale"
                    transition-hide="scale">
                    <q-date
                      type="date"
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
              v-model="event.time"
              outlined
              mask="time"
              :rules="['time']"
              class="q-mt-sm"
              label="Inserisci orario: "
              readonly>
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
          <q-btn label="Aggiungi" color="primary" @click="addEvent()" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import '@fullcalendar/core/vdom' // solves problem with Vite
import FullCalendar from '@fullcalendar/vue3'
import listPlugin from '@fullcalendar/list'
import itLocale from '@fullcalendar/core/locales/it'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'
import Heading from 'components/Heading.vue'
import moment from 'moment'
import { date } from 'quasar'

export default defineComponent({
  name: 'Calendar',
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
      selectedTasks: [],
      unselectedTasks: [],
      isGeneral: true,
      shift: '',
      operator: '',
      calendarOptions: {
        nextDayThreshold: '00:00:00',
        timeZone: 'UTC',
        height: 550,
        customButtons: {
          takeCharge: {
            text: 'Prendi in carico',
            click: this.takeCharge.bind()
          },
          aggiungi: {
            text: 'Aggiungi',
            click: this.openDialog.bind()
          }
        },
        headerToolbar: {
          right: 'today prev,next takeCharge aggiungi'
        },
        locale: itLocale,
        plugins: [listPlugin],
        initialView: 'listDay',
        handleWindowResize: true,
        events: this.fetchEvents.bind(this),
        eventClassNames: function (arg) {
          const element_colors = {
            Prelevamento: 'withdrawal',
            Accompagnamento: 'accompaniment',
            Telefonata: 'phonecall',
            Pulizia: 'clean',
            Controllo: 'control'
          }
          return [element_colors[arg.event.title]]
        }
      },
      info_dialog: false,
      eventStates: {
        open: { label: 'Da svolgere', color: 'blue' },
        charged: { label: 'Presa in carico', color: 'orange' },
        done: { label: 'Svolta', color: 'green' }
      },
      initial_tasks: [],
      guests: [],
      dialog: false,
      event: {
        guest: '',
        date: '',
        time: '',
        title: '',
        description: ''
      }
    }
  },
  mounted() {
    this.operator = JSON.parse(sessionStorage.getItem('user')).uid
    this.getShift()
  },
  methods: {
    watchDate(value, reason, detail) {
      this.event.date = moment(value).format('DD/MM/YYYY')
    },
    validate() {
      let isValid = true
      if (!this.isGeneral && !this.event?.guest) {
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
    switchConsegna(e) {
      if (e) {
        this.isGeneral = true
        delete this.event['guest']
      } else {
        this.isGeneral = false
        this.event['guest'] = null
      }
    },
    openDialog() {
      this.event = {
        title: '',
        description: '',
        start: ''
      }
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
      this.dialog = true
    },
    containsTask(obj, list) {
      const contains = list.find(e => e._id.$oid === obj._id.$oid)
      return contains !== undefined ? true : false
    },
    selectTask(task) {
      const task_to_insert = this.formatTask(task)
      const initTask = this.initial_tasks.find(
        e => e._id.$oid === task_to_insert._id.$oid
      )
      const containedUnsel = this.containsTask(
        task_to_insert,
        this.unselectedTasks
      )
      const containedSel = this.containsTask(task_to_insert, this.selectedTasks)
      if (containedUnsel && !containedSel) {
        this.unselectedTasks = this.unselectedTasks.filter(e => {
          if (e._id.$oid !== task_to_insert._id.$oid) {
            return e
          }
        })
        this.selectedTasks.push(task_to_insert)
      } else if (!containedUnsel && containedSel) {
        this.selectedTasks = this.selectedTasks.filter(e => {
          if (e._id.$oid !== task_to_insert._id.$oid) {
            return e
          }
        })
        this.unselectedTasks.push(task_to_insert)
      } else if (!containedUnsel && !containedSel) {
        if (initTask.selected) {
          this.unselectedTasks.push(task_to_insert)
        } else {
          this.selectedTasks.push(task_to_insert)
        }
      }
    },
    checkChangement() {
      this.selectedTasks = this.selectedTasks.filter(e => {
        const initial = this.initial_tasks.find(x => x._id.$oid === e._id.$oid)
        if (initial !== undefined && !initial.selected) {
          return e
        }
      })
      this.unselectedTasks = this.unselectedTasks.filter(e => {
        const initial = this.initial_tasks.find(x => x._id.$oid === e._id.$oid)
        if (initial !== undefined && initial.selected) {
          return e
        }
      })
    },
    takeCharge() {
      this.checkChangement()
      const charging_request = {}
      if (
        this.selectedTasks.length === 0 &&
        this.unselectedTasks.length === 0
      ) {
        this.showNotif(
          'warning',
          'Non è stato apportano alcun cambiamento alle consegne.'
        )
      } else {
        if (this.selectedTasks.length > 0) {
          charging_request['charge'] = this.selectedTasks.map(function (el) {
            return el._id.$oid
          })
        }
        if (this.unselectedTasks.length > 0) {
          charging_request['discharge'] = this.unselectedTasks.map(function (
            el
          ) {
            return el._id.$oid
          })
        }
        if (Object.keys(charging_request).length !== 0) {
          api
            .post('/tasks/task/charge', charging_request)
            .then(response => {
              this.showNotif(
                'positive',
                'Le consegne sono state prese in carico correttamente.'
              )
              api.post('/auth/log', {
                name: 'Presa in carico',
                description:
                  this.selectedTasks.length + ' consegne prese in carico'
              })
              const calendarApi = this.$refs.fullCalendar.getApi()
              calendarApi.refetchEvents()
            })
            .catch(err => {
              this.showNotif(
                'warning',
                'Non è stata selezionata nessuna consegna!'
              )
            })
        } else {
          this.showNotif(
            'warning',
            'Non è stato apportano alcun cambiamento alle consegne.'
          )
        }
      }
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
    fetchEvents: async function (t) {
      t = t.start
      try {
        const response = await api.get('/tasks/task', {
          params: { today_date: t }
        })
        this.initial_tasks = response.data.map(event => {
          return { ...event, allDay: true }
        })
        return response.data.map(event => {
          return { ...event, allDay: true }
        })
      } catch (exception) {
        this.showNotif(
          'negative',
          'Errore durante il caricamento delle consegne'
        )
        return []
      }
    },
    onEventClick: function (info) {
      const eventObj = { start: info.event.startStr, title: info.event.title }
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

.withdrawal .fc .fc-list-event-dot {
  border-color: orange;
}
.accompaniment .fc .fc-list-event-dot {
  border-color: green;
}
.phonecall .fc .fc-list-event-dot {
  border-color: blue;
}
.clean .fc .fc-list-event-dot {
  border-color: grey;
}
.control .fc .fc-list-event-dot {
  border-color: red !important;
}
.fc .fc-toolbar-title {
  font-size: 1.6em;
}
</style>
<style>
h5 {
  margin-top: 20px;
  margin-bottom: 30px;
}

@media (min-width: 600px) {
  .q-dialog__inner--minimized > div {
    min-width: 306px;
  }
}

td.fc-list-event-title {
  cursor: pointer;
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

.fc-view-harness.fc-view-harness-active {
  background: white;
}

.segmented {
  padding: 15px;
}

.fc-button-active {
  background-color: #567a9f !important;
}
</style>
