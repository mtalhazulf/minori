<template>
  <q-page class="q-mb-md q-mx-xl">
    <div class="row" style="height: 60px">
      <Heading :title="'Scadenzario'" />
    </div>

    <div style="display: flex; align-items: center">
      <q-dialog v-model="info_dialog">
        <q-card>
          <q-card-section>
            <div class="row">
              <div class="col-11">
                <div class="text-h6">Dettagli evento</div>
              </div>
              <div class="col-1">
                <q-icon
                  size="1.8em"
                  name="delete"
                  style="color: #f63333db"
                  @click="
                    askConfirm(
                      'Sei sicuro di voler eliminare la scadenza?',
                      deleteEvent
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
                    <q-item-label>Evento</q-item-label>
                    <q-item-label caption lines="2">{{
                      selectedEvent.title
                    }}</q-item-label>
                  </q-item-section>
                </q-item>

                <q-separator spaced inset />

                <q-item>
                  <q-item-section>
                    <q-item-label>Descrizione</q-item-label>
                    <q-item-label caption>{{
                      selectedEvent.description
                    }}</q-item-label>
                  </q-item-section>
                </q-item>
                <div v-if="'minor' in selectedEvent">
                  <q-separator spaced inset />

                  <q-item>
                    <q-item-section>
                      <q-item-label>Ospite</q-item-label>
                      <q-item-label
                        v-if="
                          typeof selectedEvent.minor === 'object' &&
                          selectedEvent.minor?.name
                        "
                        caption
                        >{{
                          selectedEvent.minor['name'] +
                          ' ' +
                          selectedEvent.minor['surname']
                        }}</q-item-label
                      >
                      <q-item-label v-else caption>
                        Nessun ospite associato
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </div>
                <q-item>
                  <q-item-section>
                    <q-item-label>Urgenza</q-item-label>
                    <q-item-label caption
                      ><q-badge
                        :color="eventStates[selectedEvent?.status].color"
                        >{{ eventStates[selectedEvent?.status].label }}</q-badge
                      ></q-item-label
                    >
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn
              v-close-popup
              flat
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
              arg.event.extendedProps?.resource
                ? arg.event.extendedProps.resource.module
                : typeof arg.event.extendedProps.minor === 'object' &&
                  arg.event.extendedProps.minor?.name
                ? arg.event.extendedProps.minor.surname.substring(0, 1) +
                  '.' +
                  arg.event.extendedProps.minor.name
                : ''
            }}
            <span
              v-if="
                arg.event.extendedProps?.resource ||
                (typeof arg.event.extendedProps.minor === 'object' &&
                  arg.event.extendedProps.minor?.name)
              ">
              -
            </span>
            <span v-if="arg.event.extendedProps.description">
              {{
                arg.event.extendedProps.description.substring(0, 15) + '...'
              }}</span
            >
            <span v-else>
              <i>{{ arg.event.title }}</i>
            </span>
          </div>
        </div>
      </template>
    </FullCalendar>
    <q-dialog v-model="dialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Aggiungi evento</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <form>
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
            <q-select
              v-model="event['minor']"
              outlined
              :options="minors"
              label="Ospite"
              class="q-mb-md"
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
            <q-select
              v-model="event['status']"
              outlined
              :options="urgency"
              emit-value
              label="Urgenza"
              class="q-mb-md">
            </q-select>
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
import { defineComponent, watchEffect } from 'vue'
import '@fullcalendar/core/vdom' // solves problem with Vite
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import itLocale from '@fullcalendar/core/locales/it'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'
import Heading from 'components/Heading.vue'
import moment from 'moment'
import { date } from 'quasar'

export default defineComponent({
  name: 'Scheduler',
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
      selectedEvents: [],
      unselectedEvents: [],
      selectedEvent: {},
      shift: '',
      operator: '',
      dialog: false,
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
        dayMaxEvents: true,
        views: {
          dayGridMonth: {
            // name of view
            dayMaxEvents: 4
            // other view-specific options here
          }
        },
        events: this.fetchEvents.bind(this),
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
    this.getShift()
  },
  methods: {
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
    openDialog() {
      this.event = {
        minor: null,
        title: '',
        description: '',
        start: '',
        status: ''
      }
      api.get('/minors/minor/all').then(response => {
        this.minors = response.data
      })
      this.dialog = true
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
        .delete('/events/' + this.selectedEvent._id.$oid)
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
      if (this.event.title === '' || this.event.title.trim() === '') {
        isValid = false
        this.showNotif('warning', 'Il campo Titolo deve essere inserito.')
      }
      if (this.event.status === '' || this.event.status.trim() === '') {
        isValid = false
        this.showNotif('warning', 'Il campo Urgenza deve essere inserito.')
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
        result.minor = result.minor ? result.minor._id.$oid : null

        api
          .post('/events', result)
          .then(resp => {
            this.showNotif(
              'positive',
              'La mansione è stata aggiunta correttamente!'
            )
            const calendarApi = this.$refs.fullCalendar.getApi()
            calendarApi.refetchEvents()
          })
          .catch(err => {
            this.showNotif('negative', 'Impossibile aggiungere la mansione!')
          })
      }
    },
    fetchEvents: async function (t) {
      t = t.start
      if (t.getDate() !== 1) {
        t.setDate(1)
        t.setMonth(t.getMonth() === 12 ? 1 : t.getMonth() + 1)
      }
      try {
        const response = await api.get('/events', {
          params: { date: t }
        })

        return response.data
      } catch (exception) {
        // storing my error onto Sentry
      }
      return []
    },
    onEventClick: async function (info) {
      const eventObj = { start: info.event.startStr, title: info.event.title }
      this.selectedEvent = Object.assign(eventObj, info.event.extendedProps)
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
</style>
