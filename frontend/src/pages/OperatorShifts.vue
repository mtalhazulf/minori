<template>
  <q-page class="q-mb-md q-mx-xl">
    <div class="row" style="height: 60px"></div>
    <div class="calendar-container">
      <FullCalendar ref="fullCalendar" :options="calendarOptions">
        <template #eventContent="arg">
          <div class="event-content">
            <span
              class="operator-color-dot"
              :style="{ backgroundColor: operatorColor }"></span>
            <span class="operator-name">{{ arg.event.title }}</span>
          </div>
        </template>
      </FullCalendar>
    </div>
    <q-dialog v-model="info_dialog">
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Dettagli turno</div>
        </q-card-section>
        <q-card-section class="q-pt-none">
          <q-list>
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
                  selectedEvent.extendedProps?.startTime
                }}</q-item-label>
              </q-item-section>
            </q-item>
            <q-separator spaced inset />
            <q-item>
              <q-item-section>
                <q-item-label>Ora fine</q-item-label>
                <q-item-label caption>{{
                  selectedEvent.extendedProps?.endTime
                }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn v-close-popup flat label="Chiudi" color="primary" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import '@fullcalendar/core/vdom'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import itLocale from '@fullcalendar/core/locales/it'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'
import moment from 'moment'

export default defineComponent({
  name: 'OperatorScheduler',
  components: {
    FullCalendar
  },
  setup() {
    const $q = useQuasar()
    return {
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
      operatorId: JSON.parse(sessionStorage.getItem('user')).uid,
      operatorName: '',
      operatorColor: '#4CAF50', // Default color
      selectedEvent: {},
      info_dialog: false,
      calendarOptions: {
        plugins: [dayGridPlugin],
        initialView: 'dayGridMonth',
        locale: itLocale,
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: ''
        },
        events: this.fetchShifts.bind(this),
        eventClick: this.onEventClick.bind(this)
      }
    }
  },
  mounted() {
    this.operatorId = JSON.parse(sessionStorage.getItem('user')).uid
    this.operatorName =
      JSON.parse(sessionStorage.getItem('user')).name +
      ' ' +
      JSON.parse(sessionStorage.getItem('user')).surname
  },
  methods: {
    async fetchShifts({ start, end }) {
      try {
        const response = await api.get('/shifts', {
          params: {
            operatorId: this.operatorId,
            start: start.toISOString(),
            end: end.toISOString()
          }
        })
        return response.data.shifts.map(shift => ({
          id: shift._id.$oid,
          title: this.operatorName,
          start: new Date(shift.date.$date),
          end: new Date(shift.date.$date),
          extendedProps: {
            startTime: new Date(shift.startTime.$date),
            endTime: new Date(shift.endTime.$date)
          }
        }))
      } catch (error) {
        console.error('Error fetching shifts:', error)
        this.showNotif('negative', 'Unable to fetch shifts')
        return []
      }
    },
    onEventClick(info) {
      this.selectedEvent = info.event
      this.info_dialog = true
    },
    formatDate(date) {
      return moment(date).format('DD/MM/YYYY')
    }
  }
})
</script>

<style scoped>
.calendar-container {
  margin-top: 20px;
}
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
</style>
