<template>
  <q-page>
    <div class="row q-mx-xl">
      <Heading :title="'Registro presenze operatori'" />
    </div>
    <div class="row q-ml-lg q-pl-lg justify-start q-mb-md">
      <q-table
        v-model:pagination="pagination"
        :rows="rows"
        :columns="columns"
        row-key="id"
        :loading="data_loading"
        :rows-per-page-options="[5, 8, 10, 15, 25, 50]">
        <template #top-right>
          <q-btn
            color="secondary"
            style="width: 150px"
            @click="
              () => {
                reset()
                dialog = true
              }
            ">
            Aggiungi Timbratura</q-btn
          >
          <q-dialog v-model="dialog" persistent>
            <q-card>
              <q-card-section>
                <div class="text-h6">Aggiungi Timbratura</div>
              </q-card-section>
              <q-card-section class="q-pt-none">
                <q-form class="q-my-sm">
                  <q-card-section>
                    <q-select
                      v-model="attendance.userId"
                      label="Operatore"
                      :options="operators.length === 0 ? [] : operators"
                      :option-label="opt => opt.name + ' ' + opt.surname"
                      emit-value
                      outlined
                      class="q-my-md"
                      ><template #no-option>
                        <q-item>
                          <q-item-section class="text-italic text-grey">
                            Nessun operatore disponibile
                          </q-item-section>
                        </q-item>
                      </template></q-select
                    >
                    <q-input
                      v-model="attendance.date"
                      outlined
                      label="Inserisci data: "
                      mask="##/##/####"
                      readonly
                      class="q-my-md">
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
                      v-model="attendance.start_date"
                      outlined
                      mask="time"
                      :rules="['time']"
                      class="q-mt-sm"
                      label="Orario inizio: "
                      readonly>
                      <template #append>
                        <q-icon name="access_time" class="cursor-pointer">
                          <q-popup-proxy
                            cover
                            transition-show="scale"
                            transition-hide="scale">
                            <q-time
                              v-model="attendance.start_date"
                              format24h
                              :options="
                                (hour, minute) =>
                                  optionsTime(attendance.date, hour, minute)
                              ">
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
                    <q-checkbox
                      v-model="startOnly"
                      label="Solo ingresso"
                      @update:model-value="clear($event)" />
                    <q-input
                      v-if="!startOnly"
                      v-model="attendance.end_date"
                      outlined
                      mask="time"
                      :rules="['time']"
                      class="q-mt-sm"
                      label="Orario fine: "
                      readonly>
                      <template #append>
                        <q-icon name="access_time" class="cursor-pointer">
                          <q-popup-proxy
                            cover
                            transition-show="scale"
                            transition-hide="scale">
                            <q-time
                              v-model="attendance.end_date"
                              format24h
                              :options="
                                (hour, minute) =>
                                  optionsTime(attendance.date, hour, minute)
                              ">
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
                  </q-card-section>
                </q-form>
              </q-card-section>

              <q-card-section align="right" class="text-primary">
                <q-btn
                  color="secondary"
                  :loading="loading"
                  style="width: 150px"
                  @click="add()">
                  Aggiungi
                  <template #loading>
                    <q-spinner-hourglass class="on-left" />
                    Loading...
                  </template>
                </q-btn>
                <q-btn
                  v-close-popup
                  label="Cancella"
                  type="reset"
                  color="primary"
                  flat
                  class="q-ml-sm"
                  @click="reset()" />
              </q-card-section>
            </q-card>
          </q-dialog>
        </template>
        <template #body="props">
          <q-tr :props="props">
            <q-td key="userId" :props="props">
              {{
                typeof props.row.userId === 'string'
                  ? props.row.userId
                  : props.row.userId?.name
                  ? props.row.userId.name + ' ' + props.row.userId.surname
                  : props.row.userId.companyName
              }}</q-td
            >
            <q-td key="userId.role" :props="props">{{
              props.row.userId?.role
                ? props.row.userId.role.name +
                  ' - ' +
                  props.row.userId.role.label
                : ''
            }}</q-td>
            <q-td key="start_date" :props="props">{{
              convertDate(props.row.start_date)
            }}</q-td>
            <q-td key="start_time" :props="props">{{
              convertHours(props.row.start_date)
            }}</q-td>
            <q-td key="end_date" :props="props">{{
              convertDate(props.row.end_date)
            }}</q-td>
            <q-td key="end_time" :props="props">
              <div
                v-if="convertHours(props.row.end_date) === true"
                class="date_slot">
                In corso
                <q-icon name="edit" size="13px" class="q-mr-lg q-ml-sm" />
                <q-popup-edit v-slot="{}" ref="popup" title="Timbra uscita">
                  <div v-if="!sameDayStampingOut" class="row">
                    <q-input
                      v-model="endAttendance.date"
                      outlined
                      label="Inserisci data: "
                      mask="##/##/####"
                      readonly
                      class="q-my-md">
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
                                  watchDateOut(value)
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
                  </div>
                  <div class="row">
                    <q-checkbox
                      v-model="sameDayStampingOut"
                      label="Stesso giorno"
                      @update:model-value="clearDateOut($event)" />
                  </div>
                  <div class="row">
                    <q-input
                      v-model="endAttendance.end_date"
                      outlined
                      mask="time"
                      :rules="['time']"
                      class="q-mt-sm"
                      label="Orario fine: "
                      readonly>
                      <template #append>
                        <q-icon name="access_time" class="cursor-pointer">
                          <q-popup-proxy
                            cover
                            transition-show="scale"
                            transition-hide="scale">
                            <q-time
                              v-model="endAttendance.end_date"
                              format24h
                              :options="
                                (hour, minute) =>
                                  optionsTime(
                                    formatDate(props.row.start_date),
                                    hour,
                                    minute
                                  )
                              ">
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
                  </div>
                  <div class="row q-mt-lg q-ml-md">
                    <q-btn
                      v-close-popup
                      flat
                      color="primary"
                      @click="endAttendance = { date: '', end_date: '' }">
                      Cancella </q-btn
                    ><q-btn
                      color="primary"
                      :disable="
                        endAttendance.end_date === '' ||
                        endAttendance.end_date.trim() === '' ||
                        (!sameDayStampingOut &&
                          endAttendance.date.trim() === '')
                      "
                      @click="stampingOut(props.row, endAttendance)">
                      Modifica
                    </q-btn>
                  </div>
                </q-popup-edit>
              </div>

              <div v-else>
                {{ convertHours(props.row.end_date) }}
              </div>
            </q-td>
            <q-td key="stamping_type" :props="props"
              ><q-badge
                rounded
                :color="
                  props.row.status === 'pending' ? 'yellow' : props.row.type
                "
                style="width: 10px"
            /></q-td>
          </q-tr>
        </template>
        <template #no-data="{ message }">
          <div class="full-width row flex-center text-primary q-gutter-sm">
            <div v-if="message === 'Loading...'">{{ message }}</div>
            <div v-else>
              <q-icon size="2em" name="sentiment_dissatisfied" />
              <span>
                {{
                  errDataMsg
                    ? 'Impossibile caricare le timbrature al momento..'
                    : 'Nessuna timbratura presente ...'
                }}
              </span>
            </div>
          </div>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import Heading from 'components/Heading.vue'
import moment from 'moment-timezone'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'
import { date } from 'quasar'

export default {
  name: 'OperatorAttendanceRegister',
  components: {
    Heading
  },
  setup() {
    const $q = useQuasar()

    return {
      optionsFn(d) {
        return d <= date.formatDate(Date.now(), 'YYYY/MM/DD')
      },
      showNotif(tp, msg) {
        $q.notify({
          type: tp,
          message: msg,
          position: 'top-right',
          timeout: 1500
        })
      }
    }
  },
  data() {
    return {
      columns: [
        {
          name: 'userId',
          align: 'center',
          label: 'Nominativo',
          field: 'name',
          sortable: true
        },
        {
          name: 'userId.role',
          label: 'Ruolo',
          align: 'center',
          field: 'userId.role',
          sortable: true
        },
        {
          name: 'start_date',
          required: true,
          label: 'Data entrata',
          align: 'center',
          field: 'start_date'
        },
        {
          name: 'start_time',
          align: 'center',
          label: 'Ora entrata',
          field: 'start_date'
        },
        {
          name: 'end_date',
          align: 'center',
          label: 'Data uscita',
          field: 'end_date'
        },
        {
          name: 'end_time',
          align: 'center',
          label: 'Ora uscita',
          field: 'end_date'
        },
        {
          name: 'stamping_type',
          align: 'center',
          label: ' Tipo',
          field: 'type'
        }
      ],
      rows: [],
      data_loading: true,
      errDataMsg: false,
      pagination: {
        page: 0,
        rowsPerPage: 8
      },
      loading: false,
      dialog: false,
      operators: [],
      attendance: {
        userId: null,
        date: '',
        start_date: '',
        end_date: ''
      },
      startOnly: true,
      end_date: '',
      sameDayStampingOut: true,
      endAttendance: {
        date: '',
        end_date: ''
      }
    }
  },
  created() {
    this.interval = setInterval(() => this.getOperatorRegister(), 100000)
  },
  mounted() {
    this.getOperatorRegister()
    this.getOperators()
  },
  unmounted() {
    clearInterval(this.interval)
  },
  methods: {
    getOperatorRegister() {
      api
        .get('/auth/attendance')
        .then(resp => {
          this.rows = resp.data
          setTimeout(() => {
            this.errDataMsg = false
            this.data_loading = false
          }, 500)
        })
        .catch(() => {
          this.errDataMsg = true
          this.data_loading = false
        })
    },
    getOperators() {
      api.get('/auth/user/operators').then(r => {
        const response = r.data.filter(el => {
          if (el.status === 'enabled' || !el?.status) {
            return el
          }
        })
        this.operators = response
      })
    },
    watchDate(value, reason, detail) {
      this.attendance.date = moment(value).format('DD/MM/YYYY')
      if (
        this.isToday(this.attendance.date) &&
        this.isGreaterThanNow(this.attendance.start_date)
      ) {
        this.attendance.start_date = ''
        this.attendance.end_date = ''
      }
    },
    watchDateOut(value) {
      this.endAttendance.date = moment(value).format('DD/MM/YYYY')
    },
    clear(e) {
      if (e) {
        this.attendance.end_date = ''
      }
    },
    clearDateOut(e) {
      if (e) {
        this.endAttendance.date = ''
      }
    },
    reset() {
      this.attendance = {
        userId: null,
        date: '',
        start_date: '',
        end_date: ''
      }
      this.startOnly = true
    },
    formatDate(data) {
      return moment(moment(data)).format('DD/MM/YYYY')
    },
    isGreaterThanNow(t) {
      const str = moment(t, 'HH:mm')
      const now = moment(moment(new Date()).format('HH:mm'), 'HH:mm')
      return str > now
    },
    isToday(d) {
      const str = moment(d, 'DD/MM/YYYY')
      const today = moment(
        moment(new Date()).format('DD/MM/YYYY'),
        'DD/MM/YYYY'
      )
      return moment(str).isSame(today)
    },
    validate() {
      let isValid = true
      if (this.attendance.userId === null) {
        isValid = false
        this.showNotif('warning', 'Inserire operatore')
      }
      if (this.attendance.date.trim() === '') {
        isValid = false
        this.showNotif('warning', 'Inserire data')
      }
      if (this.attendance.start_date.trim() === '') {
        isValid = false
        this.showNotif('warning', 'Inserire ora di inizio')
      }

      if (!this.startOnly) {
        if (this.attendance.end_date.trim() === '') {
          isValid = false
          this.showNotif('warning', 'Inserire ora di fine')
        } else {
          const start = moment(this.attendance.start_date, 'HH:mm')
          const end = moment(this.attendance.end_date, 'HH:mm')
          if (start.isSameOrAfter(end)) {
            isValid = false
            this.showNotif(
              'warning',
              "L'orario di fine non può essere uguale/precedente all'orario di inizio"
            )
          }
        }
      } else if (this.startOnly && !this.isToday(this.attendance.date)) {
        isValid = false
        this.showNotif(
          'warning',
          'Gli ingressi singoli possono essere inseriti unicamente in giornata'
        )
      }
      return isValid
    },
    resultFormatter(attendance) {
      const res = { status: 'enabled', type: 'grey' }
      res['userId'] = attendance.userId._id.$oid
      res['start_date'] =
        attendance.date + ' ' + this.convertHoursToCET(attendance.start_date)
      if (!this.startOnly) {
        res['end_date'] =
          attendance.date + ' ' + this.convertHoursToCET(attendance.end_date)
      }
      return res
    },
    add() {
      if (this.validate()) {
        const result = this.resultFormatter(this.attendance)
        this.loading = true
        api
          .post('/auth/attendance', result)
          .then(resp => {
            if (resp.data.success) {
              setTimeout(() => {
                this.loading = false
                this.showNotif('positive', 'Timbratura caricata correttamente.')
                this.dialog = false
                this.reset()
              }, 500)
              api.post('/auth/log', {
                name: 'Aggiunta timbratura: ' + this.attendance.userId.username,
                description: 'Timbratura aggiunta correttamente',
                color: 'green'
              })

              this.getOperatorRegister()
            } else if (resp.data?.msg) {
              setTimeout(() => {
                this.loading = false
                this.showNotif('warning', resp.data.msg)
              }, 500)
            }
            this.loading = false
          })
          .catch(error => {
            setTimeout(() => {
              this.loading = false
              this.showNotif(
                'negative',
                'La timbratura non è stata inserita correttamente.'
              )
              this.dialog = false
              this.reset()
            }, 500)
          })
      }
    },
    outValidate(start_date, attendance, row) {
      let isValid = true
      if (
        (!this.sameDayStampingOut && start_date === attendance.date) ||
        this.sameDayStampingOut
      ) {
        let start = row.start_date.substring(10)
        start = moment(start, 'HH:mm')
        const end = moment(attendance.end_date, 'HH:mm')
        if (start.isSameOrAfter(end)) {
          this.showNotif(
            'warning',
            "L'orario di fine non può essere uguale/precedente all'orario di inizio"
          )
          isValid = false
        }
      } else if (!this.dateIsAfter(start_date, attendance.date)) {
        isValid = false
        this.showNotif(
          'warning',
          'La data di fine deve essere successiva/uguale alla data di inizio'
        )
      }
      return isValid
    },
    stampingOut(row, attendance) {
      const start_date = this.convertDate(row.start_date.substring(0, 10))
      if (this.outValidate(start_date, attendance, row)) {
        let end_date =
          start_date + ' ' + this.convertHoursToCET(attendance.end_date)
        if (!this.sameDayStampingOut && attendance.date !== null) {
          end_date =
            attendance.date + ' ' + this.convertHoursToCET(attendance.end_date)
        }
        api
          .put('/auth/attendance/out/' + row._id.$oid, { end_date: end_date })
          .then(resp => {
            if (resp.data.success) {
              setTimeout(() => {
                this.showNotif('positive', 'Uscita timbrata correttamente.')
              }, 500)
              this.getOperatorRegister()
            } else if (resp.data?.msg) {
              setTimeout(() => {
                this.showNotif('warning', resp.data.msg)
              }, 500)
            }
          })
          .catch(error => {
            setTimeout(() => {
              this.showNotif(
                'negative',
                "L'uscita non è stata inserita correttamente."
              )
            }, 500)
          })
      }
    },
    optionsTime(att, h, m) {
      if (att.trim() !== '' && this.isToday(att)) {
        return !this.isGreaterThanNow(h + ':' + (m === null ? '00' : m))
      } else {
        return true
      }
    },
    convertDate(date) {
      if (!date) return '-'
      return moment(String(date)).format('DD/MM/YYYY')
    },
    convertHours(date) {
      if (date) {
        return moment.tz(date, 'Europe/Rome').format('HH:mm')
      } else {
        return true
      }
    },
    convertHoursToCET(date) {
      return moment.tz(date, 'HH:mm', 'Europe/Rome').format('HH:mm')
    },
    dateIsAfter(start_date, end_date) {
      if (
        moment(start_date, 'DD/MM/YYYY').diff(
          moment(end_date, 'DD/MM/YYYY'),
          'days'
        ) <= 0
      ) {
        return true
      } else {
        return false
      }
    }
  }
}
</script>

<style scoped>
.sign {
  width: 130px;
  height: 80px;
}

.q-table__container.q-table--horizontal-separator.column.no-wrap.q-table__card.q-table--no-wrap {
  width: 98%;
}

.date_slot {
  cursor: pointer;
}
</style>
