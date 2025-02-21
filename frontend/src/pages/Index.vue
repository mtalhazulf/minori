<template>
  <q-page>
    <div class="row q-mx-xl">
      <Heading :title="'Dashboard'" />
    </div>
    <div class="row q-ml-md">
      <q-card
        class="my-card q-ml-md"
        style="width: 25%; overflow-x: hidden; overflow-y: hidden">
        <q-card-section>
          <q-list style="width: 100%">
            <q-item>
              <q-item-section>Operatori presenti : </q-item-section>
            </q-item>

            <q-separator color="black" inset />
            <div v-if="operators.length > 0">
              <q-scroll-area
                style="height: 175px"
                :visible="operators.length > 3">
                <q-item
                  v-for="op in operators"
                  :key="op._id"
                  style="width: max-content; min-width: 100%">
                  <q-item-section avatar>
                    <q-avatar
                      size="30px"
                      class="shadow-2"
                      color="white"
                      text-color="grey"
                      font-size="40px"
                      icon="person" />
                  </q-item-section>
                  <q-item-section>{{
                    op.name + ' ' + op.surname
                  }}</q-item-section>
                  <q-item-section
                    v-if="
                      (operator.usertype === 'admin' ||
                        operator.usertype === 'superadmin') &&
                      op.status === 'pending'
                    ">
                    <div
                      style="
                        display: flex;
                        justify-content: end;
                        flex-direction: row;
                      ">
                      <q-btn
                        color="green"
                        text-color="white"
                        label="Accetta"
                        class="accept_refuse_btn"
                        style="margin-right: 10px"
                        @click="
                          () => {
                            selectedOperatorAttendance = op
                            operatorAttendanceDialog = true
                          }
                        " />
                      <q-btn
                        color="red"
                        text-color="white"
                        class="accept_refuse_btn"
                        label="Rifiuta"
                        style="margin-right: 25px"
                        @click="changeOpStatus(op._id.$oid, 'refused')" />
                    </div>
                  </q-item-section>
                  <q-item-section
                    v-else-if="op.status === 'refused'"
                    class="dots"
                    ><q-badge rounded color="red" style="width: 10px"
                  /></q-item-section>
                  <q-item-section
                    v-else-if="op.status === 'pending'"
                    class="dots"
                    ><q-badge rounded color="yellow" style="width: 10px"
                  /></q-item-section>
                  <q-item-section v-else class="dots"
                    ><q-badge rounded color="green" style="width: 10px"
                  /></q-item-section>
                </q-item>
              </q-scroll-area>
            </div>
            <div v-else class="q-pl-md">Nessun operatore attivo al momento</div>
          </q-list>
        </q-card-section>
      </q-card>
      <q-card id="carta2" class="my-card q-ml-md" style="width: 35%">
        <q-card-section>
          <q-list style="min-width: 250px; width: 100%">
            <q-item>
              <q-item-section>Attività turno : </q-item-section>
            </q-item>

            <q-separator color="black" inset />
            <q-item class="withPadding">
              <q-linear-progress
                size="20px"
                :value="
                  getLoading(
                    tasks + notebookTasks,
                    takenTasks + takenNotebookTasks
                  )
                "
                color="secondary">
                <div class="absolute-full flex flex-center">
                  <q-badge
                    color="white"
                    text-color="accent"
                    :label="
                      'Diario di bordo  (' +
                      (
                        getLoading(
                          tasks + notebookTasks,
                          takenTasks + takenNotebookTasks
                        ) * 100
                      )
                        .toString()
                        .substring(0, 4) +
                      '%)'
                    " />
                </div>
              </q-linear-progress>
            </q-item>
            <q-item class="withPadding">
              <q-linear-progress
                size="20px"
                :value="getLoading(notebookTasks, takenNotebookTasks)"
                color="warning">
                <div class="absolute-full flex flex-center">
                  <q-badge
                    color="white"
                    text-color="accent"
                    :label="
                      'Mansionario  (' +
                      (getLoading(notebookTasks, takenNotebookTasks) * 100)
                        .toString()
                        .substring(0, 4) +
                      '%)'
                    " />
                </div>
              </q-linear-progress>
            </q-item>
            <q-item class="withPadding">
              <q-linear-progress
                size="20px"
                :value="getLoading(tasks, takenTasks)"
                color="accent">
                <div class="absolute-full flex flex-center">
                  <q-badge
                    color="white"
                    text-color="accent"
                    :label="
                      'Quaderno delle consegne (' +
                      (getLoading(tasks, takenTasks) * 100)
                        .toString()
                        .substring(0, 4) +
                      '%)'
                    " />
                </div>
              </q-linear-progress>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>
      <q-card id="carta2" class="my-card q-ml-md" style="width: 30%">
        <q-card-section>
          <q-list style="width: 100%">
            <q-item>
              <q-item-section>Scadenze Farmaci : </q-item-section>
            </q-item>

            <q-separator color="black" inset />

            <div
              v-if="medicinal_expirations && medicinal_expirations.length > 0">
              <q-scroll-area
                style="height: 185px"
                :visible="medicinal_expirations.length > 3">
                <q-item
                  v-for="medicinal in medicinal_expirations"
                  :key="medicinal._id"
                  style="width: max-content; min-width: 100%">
                  <q-item-section avatar>
                    <q-avatar>
                      <q-badge
                        rounded
                        :color="
                          getDaysToExpire(medicinal.expiration_date) < 15
                            ? 'red'
                            : 'yellow'
                        " />
                    </q-avatar>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label lines="1">{{ medicinal.name }}</q-item-label>
                    <q-item-label caption lines="2">
                      Scadenza: {{ convertDate(medicinal.expiration_date) }}
                    </q-item-label>
                  </q-item-section>
                  <q-item-section side top>
                    <q-item-label lines="1"
                      ><span class="text-weight-bold"
                        >Attenzione!</span
                      ></q-item-label
                    >
                    <q-item-label caption lines="2"
                      >Scade tra
                      {{ getDaysToExpire(medicinal.expiration_date) }}
                      giorni</q-item-label
                    >
                  </q-item-section>
                </q-item>
              </q-scroll-area>
            </div>
            <div v-else class="q-pl-md">
              Non è presente nessuna scadenza per il momento
            </div>
          </q-list>
        </q-card-section>
      </q-card>
    </div>

    <div class="row q-mt-lg q-ml-md">
      <q-card class="my-card q-ml-md">
        <q-card-section>
          <q-list style="max-width: 250px; width: 100%">
            <q-item>
              <q-item-section>Mansioni : </q-item-section>
            </q-item>

            <q-separator color="black" inset />

            <q-item>
              <q-item-section avatar>
                <q-avatar>
                  <q-badge rounded color="yellow" :label="takenNotebookTasks" />
                </q-avatar>
              </q-item-section>
              <q-item-section>Prese in carico</q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-avatar>
                  <q-badge rounded color="green" :label="doneNotebookTasks" />
                </q-avatar>
              </q-item-section>
              <q-item-section>Svolte</q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-avatar>
                  <q-badge
                    rounded
                    color="red"
                    :label="notebookTasks - takenNotebookTasks" />
                </q-avatar>
              </q-item-section>
              <q-item-section>Non effettuate</q-item-section>
            </q-item>
            <q-item>
              <q-item-section>Totali : {{ notebookTasks }}</q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>
      <q-card class="my-card q-ml-md">
        <q-card-section>
          <q-list style="max-width: 250px; width: 100%">
            <q-item>
              <q-item-section>Consegne : </q-item-section>
            </q-item>

            <q-separator color="black" inset />

            <q-item>
              <q-item-section avatar>
                <q-avatar>
                  <q-badge rounded color="yellow" :label="takenTasks" />
                </q-avatar>
              </q-item-section>
              <q-item-section>Prese in carico</q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-avatar>
                  <q-badge rounded color="green" :label="doneTasks" />
                </q-avatar>
              </q-item-section>
              <q-item-section>Svolte</q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-avatar>
                  <q-badge rounded color="red" :label="tasks - takenTasks" />
                </q-avatar>
              </q-item-section>
              <q-item-section>Non effettuate</q-item-section>
            </q-item>
            <q-item>
              <q-item-section>Totali : {{ tasks }}</q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>
      <q-card id="carta" class="my-card q-ml-md">
        <q-card-section>
          <q-list style="min-width: 250px; width: 100%">
            <q-item>
              <q-item-section>Attività : </q-item-section>
            </q-item>

            <q-separator color="black" inset />
            <div v-if="activities.length > 0">
              <q-scroll-area
                style="height: 185px"
                :visible="activities.length > 3">
                <q-item v-for="activity in activities" :key="activity._id">
                  <q-item-section avatar>
                    <q-avatar>
                      <q-badge
                        rounded
                        :color="
                          'color' in activity ? activity.color : 'yellow'
                        " />
                    </q-avatar>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label lines="1">{{ activity.name }}</q-item-label>
                    <q-item-label caption lines="2">
                      {{ activity.description }}
                    </q-item-label>
                  </q-item-section>

                  <q-item-section side top>
                    <q-item-label lines="1"
                      ><span class="text-weight-bold">{{
                        typeof activity.operator === 'string'
                          ? activity.operator
                          : activity.operator?.name
                          ? activity.operator.name +
                            ' ' +
                            activity.operator.surname
                          : activity.operator.companyName
                      }}</span></q-item-label
                    >
                    <q-item-label caption lines="2">{{
                      utcToLocalTime(activity.hour)
                    }}</q-item-label>
                  </q-item-section>
                </q-item>
              </q-scroll-area>
            </div>
            <div v-else class="q-pl-md">
              Non è stata eseguita alcuna attività per il momento
            </div>
          </q-list>
        </q-card-section>
      </q-card>
    </div>
    <q-dialog v-model="operatorAttendanceDialog" persistent>
      <q-card>
        <q-card-section>
          <div class="text-h6">Selezionare l'orario di entrata</div>
        </q-card-section>
        <q-card-section class="q-pt-none">
          <form>
            <q-input
              v-model="selectedOperatorAttendanceStartTime"
              mask="time"
              :rules="['time']">
              <template #append>
                <q-icon name="access_time" class="cursor-pointer">
                  <q-popup-proxy
                    cover
                    transition-show="scale"
                    transition-hide="scale">
                    <q-time
                      v-model="selectedOperatorAttendanceStartTime"
                      :options="(hour, minute) => optionsTime(hour, minute)"
                      format24h>
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
            flat
            label="Annulla"
            color="primary"
            @click="
              () => {
                operatorAttendanceDialog = false
                selectedOperatorAttendance = {}
              }
            " />
          <q-btn
            flat
            label="Accetta"
            color="positive"
            @click="
              changeOpStatus(
                selectedOperatorAttendance._id.$oid,
                'enabled',
                selectedOperatorAttendanceStartTime
              )
            " />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import Heading from 'components/Heading.vue'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'
import moment from 'moment-timezone'

export default defineComponent({
  name: 'PageIndex',
  components: {
    Heading
  },
  setup() {
    const $q = useQuasar()

    return {
      showNotif(t, msg, pos = 'top-right', timeout = 2000) {
        $q.notify({
          type: t,
          message: msg,
          position: pos,
          timeout: timeout,
          multiLine: true
        })
      }
    }
  },
  data() {
    return {
      operators: [],
      selectedOperatorAttendance: {},
      selectedOperatorAttendanceStartTime: moment().format('HH:mm'),
      operatorAttendanceDialog: false,
      notebookTasks: 0,
      takenNotebookTasks: 0,
      doneNotebookTasks: 0,
      tasks: 0,
      takenTasks: 0,
      doneTasks: 0,
      activities: [],
      medicinal_expirations: [],
      operator: '',
      todayDayName: new Date().toLocaleDateString('it-IT', {
        weekday: 'short'
      })
    }
  },
  mounted() {
    this.operator = JSON.parse(sessionStorage.getItem('user'))
    this.getActiveOperators()
    this.getActivities()
    this.getMedicinal()
    this.getTasksInfo()
    if (this.operator.usertype !== 'user') {
      this.getScheduleEvents()
    }
    this.resetTasks()
  },
  methods: {
    utcToLocalTime(timeStr) {
      // take a time in UTC like "10:00" and return it in local time
      const hours = parseInt(timeStr.split(':')[0])
      const minutes = parseInt(timeStr.split(':')[1])
      const now = new Date()
      const offset = now.getTimezoneOffset() / 60
      const newHours = (hours - offset) % 24
      return `${newHours.toString().padStart(2, '0')}:${minutes
        .toString()
        .padStart(2, '0')}`
    },
    resetTasks() {
      api.get('/tasks/notebook/reset')
    },
    optionsTime(h, m) {
      const now = new Date()
      const hours = now.getHours()
      const minutes = now.getMinutes()
      if (h < hours) {
        return true
      } else if (h === hours && m < minutes) {
        return true
      }
      return false
    },
    getLoading(total, done) {
      if (total === 0) {
        return 0
      } else {
        return done / total
      }
    },
    getShift() {
      const now = new Date().getHours()
      if (now >= 0 && now <= 14) {
        return 'Mattina'
      } else if (now > 14 && now <= 18) {
        return 'Pomeriggio'
      } else {
        return 'Sera'
      }
    },
    getTasksInfo() {
      api
        .get('/tasks/task/summary')
        .then(response => {
          this.tasks = response.data.total
          this.takenTasks = response.data.taken
          this.doneTasks = response.data.done
        })
        .catch(() => {
          this.tasks = 0
          this.takenTasks = 0
          this.doneTasks = 0
        })

      api
        .get(
          '/tasks/notebook/summary/' + this.getShift() + '/' + this.todayDayName
        )
        .then(response => {
          this.notebookTasks = response.data.total
          this.takenNotebookTasks = response.data.taken
          this.doneNotebookTasks = response.data.done
        })
        .catch(() => {
          this.notebookTasks = 0
          this.takenNotebookTasks = 0
          this.doneNotebookTasks = 0
        })
    },
    getActivities() {
      api
        .get('/auth/log')
        .then(response => {
          this.activities = response.data
        })
        .catch(() => {
          this.activities = []
        })
    },
    getMedicinal() {
      let today = new Date()
      today = moment(String(today)).format('DD/MM/YYYY')
      api
        .get(`/tasks/medication?page=0&limit=8&expiration_date=${today}`)
        .then(response => {
          this.medicinal_expirations = response?.data?.paginatedResults
        })
        .catch(() => {
          this.medicinal_expirations = []
        })
    },
    getActiveOperators() {
      api
        .get('/auth/attendance/status')
        .then(response => {
          this.operators = response.data
        })
        .catch(error => {})
    },
    getScheduleEvents() {
      api
        .get('/events/expiring')
        .then(response => {
          if (response.data) {
            if (response.data?.expiring) {
              this.showNotif(
                'warning',
                `Controllare lo scadenzario! Sono presenti ${response.data?.count} eventi in scadenza nei prossimi 15 giorni.`,
                'bottom-right',
                5000
              )
            }
          }
        })
        .catch(error => {})
    },
    changeOpStatus(id, status, start_date = undefined) {
      const start_date_formatted = start_date
        ? moment().format('DD/MM/YYYY') +
          ' ' +
          this.selectedOperatorAttendanceStartTime
        : undefined
      api
        .put('/auth/attendance', {
          user: id,
          status: status,
          start_date: start_date_formatted
        })
        .then(response => {
          if (status === 'enabled') {
            this.showNotif(
              'positive',
              "La richiesta dell'operatore è stata accettata. Adesso potrà accedere all'applicazione"
            )
          } else {
            this.showNotif(
              'positive',
              "La richiesta dell'operatore è stata rifiutata."
            )
          }
          this.operatorAttendanceDialog = false
          this.getActiveOperators()
        })
    },
    convertDate(date) {
      return moment(String(date)).format('DD/MM/YYYY')
    },
    getDaysToExpire(data) {
      const dateofvisit = moment(data)
      const today = moment()
      return Math.ceil(dateofvisit.diff(today, 'days', true))
    }
  }
})
</script>
<style scoped>
.q-card.my-card {
  height: 265px;
  width: 20%;
}
.q-item {
  padding-top: 0px;
  padding-bottom: 0px;
}
.q-separator {
  margin-bottom: 10px;
}

#carta {
  width: 50%;
}

#carta2 {
  width: 71%;
}

.withPadding {
  padding-top: 15px;
}

.q-item__section.column.q-item__section--main.justify-center.dots {
  display: flex;
  justify-content: center;
  align-items: flex-end;
}

.accept_refuse_btn {
  padding-left: 8px;
  padding-right: 8px;
}

.accept_refuse_col {
  display: flex;
  justify-content: end;
}
</style>
