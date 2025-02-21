<template>
  <q-page class="q-mx-xl">
    <div class="row"><Heading :title="'Reportistica'" /></div>
    <div class="row">
      <div class="q-gutter-y-md" style="width: 100%">
        <q-card class="my-card">
          <q-card-section>
            <div class="row">
              <div class="text-h6 col-11">Export Farmaci</div>
              <div class="col-1 text-right">
                <q-btn
                  color="primary"
                  size="0.7em"
                  :icon="exportToggle[0] ? 'filter_alt_off' : 'filter_alt'"
                  @click="
                    () => {
                      exportToggle[0] = !exportToggle[0]
                      if (!exportToggle[0]) {
                        medicationFilters.expired = null
                        medicationFilters.disposed_of = null
                      }
                    }
                  " />
              </div>
            </div>
            <div class="text-subtitle2 text-grey-8">
              Permette l'esportazione (pdf) dei farmaci inseriti
            </div>
          </q-card-section>

          <q-card-section v-if="exportToggle[0]">
            <div class="row">
              <q-select
                v-model="medicationFilters.expired"
                outlined
                :options="medicationOptions"
                label="Scadenza"
                clearable
                style="width: 20%"
                emit-value
                ><template #selected-item="scope">
                  {{ medicationOptions.find(x => x.value === scope.opt).label }}
                </template></q-select
              >
              <q-select
                v-model="medicationFilters.disposed_of"
                outlined
                :options="medicationOptionsDisposed"
                label="Smaltimento"
                clearable
                style="width: 20%"
                class="q-ml-sm"
                emit-value
                ><template #selected-item="scope">
                  {{
                    medicationOptionsDisposed.find(x => x.value === scope.opt)
                      .label
                  }}
                </template></q-select
              >
            </div>
          </q-card-section>

          <q-separator v-if="exportToggle[0]" dark />

          <q-card-actions>
            <q-space />
            <q-btn
              color="green"
              :loading="loadingExp[0]"
              @click="
                exportPdf('medication', 'Farmaci', true, 0, medicationFilters)
              "
              >Export PDF
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
            <q-btn
              color="purple"
              :loading="loadingShow[0]"
              @click="
                exportPdf('medication', 'Farmaci', false, 0, medicationFilters)
              "
              >Visualizza
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
          </q-card-actions> </q-card
        ><q-card class="my-card">
          <q-card-section>
            <div class="row">
              <div class="text-h6 col-11">Export Presenze Operatori</div>
              <div class="col-1 text-right">
                <q-btn
                  color="primary"
                  size="0.7em"
                  :icon="exportToggle[1] ? 'filter_alt_off' : 'filter_alt'"
                  @click="
                    () => {
                      exportToggle[1] = !exportToggle[1]
                      if (!exportToggle[1]) {
                        opAttendancesFilters.start_date = null
                        opAttendancesFilters.end_date = null
                        opAttendancesFilters.operator = null
                      }
                    }
                  " />
              </div>
            </div>
            <div class="text-subtitle2 text-grey-8">
              Permette l'esportazione (pdf) delle timbrature effettuate dagli
              operatori
            </div>
          </q-card-section>

          <q-card-section v-if="exportToggle[1]">
            <div class="row">
              <q-input
                :model-value="opAttendancesFilters.start_date"
                type="text"
                outlined
                class="q-ma-sm"
                label="Inserisci data di inizio: "
                readonly>
                <template #append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy
                      ref="qDateProxy"
                      cover
                      transition-show="scale"
                      transition-hide="scale">
                      <q-date
                        :locale="locale"
                        :model-value="opAttendancesFilters.start_date"
                        mask="DD/MM/YYYY"
                        type="date"
                        @update:model-value="
                          (value, reason, detail) => {
                            watchDate(
                              value,
                              'start_date',
                              'opAttendancesFilters'
                            )
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
                :model-value="opAttendancesFilters.end_date"
                type="text"
                outlined
                class="q-ma-sm"
                label="Inserisci data di fine: "
                readonly>
                <template #append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy
                      ref="qDateProxy"
                      cover
                      transition-show="scale"
                      transition-hide="scale">
                      <q-date
                        :locale="locale"
                        :model-value="opAttendancesFilters.end_date"
                        mask="DD/MM/YYYY"
                        type="date"
                        @update:model-value="
                          (value, reason, detail) => {
                            watchDate(value, 'end_date', 'opAttendancesFilters')
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
              <q-select
                v-model="opAttendancesFilters.operator"
                outlined
                clearable
                class="q-ma-sm"
                label="Operatore"
                :options="operators.length === 0 ? [] : operators"
                :option-label="opt => opt.name + ' ' + opt.surname"
                emit-value
                style="width: 20%"
                ><template #no-option>
                  <q-item>
                    <q-item-section class="text-italic text-grey">
                      Nessun operatore disponibile
                    </q-item-section>
                  </q-item>
                </template></q-select
              >
            </div>
          </q-card-section>

          <q-separator v-if="exportToggle[1]" dark />

          <q-card-actions>
            <q-space />
            <q-btn
              color="green"
              :loading="loadingExp[1]"
              @click="
                exportPdf(
                  'operators',
                  'Timbrature',
                  true,
                  1,
                  opAttendancesFilters
                )
              "
              >Export PDF
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
            <q-btn
              color="purple"
              :loading="loadingShow[1]"
              @click="
                exportPdf(
                  'operators',
                  'Timbrature',
                  false,
                  1,
                  opAttendancesFilters
                )
              "
              >Visualizza
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
          </q-card-actions>
        </q-card>
        <q-card class="my-card">
          <q-card-section>
            <div class="row">
              <div class="text-h6 col-11">Esportazione Presenze Ospiti</div>
              <div class="col-1 text-right">
                <q-btn
                  color="primary"
                  size="0.7em"
                  :icon="exportToggle[2] ? 'filter_alt_off' : 'filter_alt'"
                  @click="
                    () => {
                      exportToggle[2] = !exportToggle[2]
                      if (!exportToggle[2]) {
                        minorAttendancesFilters.date = null
                      }
                    }
                  " />
              </div>
            </div>
            <div class="text-subtitle2 text-grey-8">
              Permette l'esportazione (pdf) delle presenze degli ospiti del mese
              corrente
            </div>
          </q-card-section>

          <q-card-section v-if="exportToggle[2]">
            <q-input
              :model-value="minorAttendancesFilters.date"
              type="text"
              outlined
              class="q-ma-sm"
              label="Inserisci mese: "
              mask="##/####"
              readonly
              style="width: 20%">
              <template #append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy
                    ref="monthPicker"
                    cover
                    transition-show="scale"
                    transition-hide="scale">
                    <q-date
                      :locale="locale"
                      default-view="Years"
                      mask="MM/YYYY"
                      type="date"
                      :model-value="minorAttendancesFilters.date"
                      emit-immediately
                      @update:model-value="
                        (value, reason) => {
                          watchMonthDate(
                            value,
                            reason,
                            'minorAttendancesFilters'
                          )
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
          </q-card-section>

          <q-separator v-if="exportToggle[2]" dark />

          <q-card-actions>
            <q-space />
            <q-btn
              color="green"
              :loading="loadingExp[2]"
              @click="
                exportPdf(
                  'minors',
                  'Presenze ospiti',
                  true,
                  2,
                  minorAttendancesFilters
                )
              "
              >Export PDF
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
            <q-btn
              color="purple"
              :loading="loadingShow[2]"
              @click="
                exportPdf(
                  'minors',
                  'Presenze ospiti',
                  false,
                  2,
                  minorAttendancesFilters
                )
              "
              >Visualizza
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
          </q-card-actions>
        </q-card>
        <q-card class="my-card q-my-md">
          <q-card-section>
            <div class="row">
              <div class="text-h6 col-11">Export Telefonate</div>
              <div class="col-1 text-right">
                <q-btn
                  color="primary"
                  size="0.7em"
                  :icon="exportToggle[3] ? 'filter_alt_off' : 'filter_alt'"
                  @click="
                    () => {
                      exportToggle[3] = !exportToggle[3]
                      if (!exportToggle[3]) {
                        callFilters.start_date = null
                        callFilters.end_date = null
                        callFilters.minor = null
                        callFilters.operator = null
                      }
                    }
                  " />
              </div>
            </div>
            <div class="text-subtitle2 text-grey-8">
              Permette l'esportazione (pdf) del registro telefonate
            </div>
          </q-card-section>

          <q-card-section v-if="exportToggle[3]">
            <div class="row">
              <q-input
                :model-value="callFilters.start_date"
                type="text"
                outlined
                class="q-ma-sm"
                label="Inserisci data di inizio: "
                readonly>
                <template #append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy
                      ref="qDateProxy"
                      cover
                      transition-show="scale"
                      transition-hide="scale">
                      <q-date
                        :locale="locale"
                        :model-value="callFilters.start_date"
                        mask="DD/MM/YYYY"
                        type="date"
                        @update:model-value="
                          value => {
                            watchDate(value, 'start_date', 'callFilters')
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
                :model-value="callFilters.end_date"
                type="text"
                outlined
                class="q-ma-sm"
                label="Inserisci data di fine: "
                readonly>
                <template #append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy
                      ref="qDateProxy"
                      cover
                      transition-show="scale"
                      transition-hide="scale">
                      <q-date
                        :locale="locale"
                        :model-value="callFilters.end_date"
                        mask="DD/MM/YYYY"
                        type="date"
                        @update:model-value="
                          value => {
                            watchDate(value, 'end_date', 'callFilters')
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
              <q-select
                v-model="callFilters.operator"
                outlined
                class="q-ma-sm"
                label="Operatore"
                clearable
                :options="operators.length === 0 ? [] : operators"
                :option-label="opt => opt.name + ' ' + opt.surname"
                emit-value
                style="width: 20%"
                ><template #no-option>
                  <q-item>
                    <q-item-section class="text-italic text-grey">
                      Nessun operatore disponibile
                    </q-item-section>
                  </q-item>
                </template></q-select
              >
              <q-select
                ref="selectMinor"
                v-model="callFilters.minor"
                outlined
                :options="minors"
                label="Ospite"
                clearable
                emit-value
                map-options
                class="q-ma-sm"
                :option-label="opt => opt.name + ' ' + opt.surname"
                :option-value="opt => opt._id.$oid"
                style="width: 20%">
                <template #no-option>
                  <q-item>
                    <q-item-section class="text-italic text-grey">
                      Non sono presenti ospiti
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>
            </div>
          </q-card-section>

          <q-separator v-if="exportToggle[3]" dark />

          <q-card-actions>
            <q-space />
            <q-btn
              color="green"
              :loading="loadingExp[3]"
              @click="
                exportPdf('call-logs', 'Telefonate', true, 3, callFilters)
              "
              >Export PDF
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
            <q-btn
              color="purple"
              :loading="loadingShow[3]"
              @click="
                exportPdf('call-logs', 'Telefonate', false, 3, callFilters)
              "
              >Visualizza
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
          </q-card-actions>
        </q-card>
        <!-- TODO controllare Export diario di bordo e forse rimuovere Export Moduli HCCP -->
        <!-- <q-card class="my-card q-my-md">
          <q-card-section>
            <div class="row">
              <div class="text-h6 col-11">Export Moduli HCCP</div>
              <div class="col-1 text-right">
                <q-btn
                  color="primary"
                  size="0.7em"
                  :icon="
                    hccpFilters.date === null ? 'filter_alt' : 'filter_alt_off'
                  "
                  @click="
                    () => {
                      if (hccpFilters.date !== null) {
                        hccpFilters.date = null
                      }
                    }
                  " />
              </div>
            </div>
            <div class="text-subtitle2 text-grey-8">
              Permette l'esportazione (pdf) dei moduli hccp scelti
            </div>
          </q-card-section> 

          <q-card-section>
            <div class="row">
              <q-select
                v-model="hccpFilters.type"
                outlined
                :options="hccpOptions"
                label="Modulo"
                style="width: 40%"
                emit-value
                ><template #selected-item="scope">
                  {{ scope.opt.label }}
                </template></q-select
              >
              <q-input
                v-model="hccpFilters.date"
                outlined
                class="q-ml-sm"
                label="Inserisci mese: "
                mask="##/####"
                readonly
                style="width: 40%">
                <template #append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy
                      ref="monthPicker"
                      cover
                      transition-show="scale"
                      transition-hide="scale">
                      <q-date :locale="locale" 
                        emit-immediately
                        default-view="Years"
                        mask="YYYY/MM"
                        type="date"
                        @update:model-value="
                          (value, reason, detail) => {
                            watchMonthDate(value, reason, 'hccpFilters')
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
          </q-card-section>

          <q-separator dark />

          <q-card-actions>
            <q-space />
            <q-btn
              color="green"
              :loading="loadingExp[4]"
              @click="
                validateHccp() &&
                  exportPdf('hccp', 'HCCP', true, 4, hccpFilters)
              "
              >Export PDF
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
            <q-btn
              color="purple"
              :loading="loadingShow[4]"
              @click="
                validateHccp() &&
                  exportPdf('hccp', 'HCCP', false, 4, hccpFilters)
              "
              >Visualizza
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
          </q-card-actions>
        </q-card>-->
        <q-card class="my-card q-my-md">
          <q-card-section>
            <div class="row">
              <div class="text-h6 col-11">Export Diario di bordo</div>
              <div class="col-1 text-right">
                <q-btn
                  color="primary"
                  size="0.7em"
                  :icon="exportToggle[5] ? 'filter_alt_off' : 'filter_alt'"
                  @click="
                    () => {
                      exportToggle[5] = !exportToggle[5]
                      if (!exportToggle[5]) {
                        logbookFilters.date = null
                        logbookFilters.operator = null
                      }
                    }
                  " />
              </div>
            </div>
            <div class="text-subtitle2 text-grey-8">
              Permette l'esportazione (pdf) delle note del diario di bordo
            </div>
          </q-card-section>

          <q-card-section v-if="exportToggle[5]">
            <div class="row">
              <q-input
                :model-value="logbookFilters.date"
                type="text"
                outlined
                class="q-ma-sm"
                label="Inserisci data: "
                readonly>
                <template #append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy
                      ref="qDateProxy"
                      cover
                      transition-show="scale"
                      transition-hide="scale">
                      <q-date
                        :locale="locale"
                        :model-value="logbookFilters.date"
                        type="date"
                        mask="DD/MM/YYYY"
                        @update:model-value="
                          value => {
                            watchDate(value, 'date', 'logbookFilters')
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
              <q-select
                v-model="logbookFilters.operator"
                outlined
                class="q-ma-sm"
                label="Operatore"
                :options="operators.length === 0 ? [] : operators"
                :option-label="opt => opt.name + ' ' + opt.surname"
                emit-value
                clearable
                style="width: 20%"
                ><template #no-option>
                  <q-item>
                    <q-item-section class="text-italic text-grey">
                      Nessun operatore disponibile
                    </q-item-section>
                  </q-item>
                </template></q-select
              >
            </div>
          </q-card-section>

          <q-separator v-if="exportToggle[5]" dark />

          <q-card-actions>
            <q-space />
            <q-btn
              color="green"
              :loading="loadingExp[5]"
              @click="
                exportPdf('logbook', 'Diario di bordo', true, 5, logbookFilters)
              "
              >Export PDF
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
            <q-btn
              color="purple"
              :loading="loadingShow[5]"
              @click="
                exportPdf(
                  'logbook',
                  'Diario di bordo',
                  false,
                  5,
                  logbookFilters
                )
              "
              >Visualizza
              <template #loading>
                <q-spinner color="white" size="1em" />
              </template>
            </q-btn>
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import Heading from 'components/Heading.vue'
import { useQuasar } from 'quasar'
import moment from 'moment'
import { api } from 'src/boot/axios'
import { date } from 'quasar'
import { itLocaleQDate } from 'src/const/QDateItLocale'

export default {
  name: 'Reports',
  components: {
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
          timeout: 1500
        })
      }
    }
  },
  data() {
    return {
      locale: itLocaleQDate,
      loadingExp: [false, false, false, false, false, false],
      loadingShow: [false, false, false, false, false, false],
      exportToggle: [false, false, false, false, true, false],
      medicationFilters: {
        expired: null,
        disposed_of: null
      },
      opAttendancesFilters: {
        start_date: null,
        end_date: null,
        operator: null
      },
      minorAttendancesFilters: {
        date: null
      },
      callFilters: {
        start_date: null,
        end_date: null,
        operator: null,
        minor: null
      },
      hccpFilters: {
        type: null,
        date: null
      },
      logbookFilters: {
        date: null,
        operator: null
      },
      operators: [],
      minors: [],
      medicationOptions: [
        { label: 'Scaduti', value: true },
        { label: 'Non scaduti', value: false }
      ],
      medicationOptionsDisposed: [
        { label: 'Smaltiti', value: true },
        { label: 'Non smaltiti', value: false }
      ],
      hccpOptions: []
    }
  },
  mounted() {
    this.getOperators()
    this.getMinors()
    this.getHccpModules()
  },
  methods: {
    getOperators() {
      api.get('/auth/user/operators').then(response => {
        this.operators = response.data
      })
    },
    getMinors() {
      api.get('/minors/minor/all').then(response => {
        this.minors = response.data
      })
    },
    getHccpModules() {
      api.get('/settings/setting/task').then(response => {
        this.hccpOptions = response.data
      })
    },
    validateHccp() {
      if (this.hccpFilters.type === null) {
        this.showNotif('warning', 'Inserire tipologia modulo')
        return false
      } else {
        return true
      }
    },
    validate(variable, end_date) {
      if (this[variable].start_date !== null && end_date !== null) {
        if (
          moment(this[variable].start_date, 'DD/MM/YYYY').isAfter(
            moment(end_date, 'DD/MM/YYYY')
          )
        ) {
          this.showNotif(
            'warning',
            'La data di fine non può essere precedente a quella di inizio'
          )

          return false
        }
      }
      return true
    },
    dataURItoBlob(dataURI) {
      const byteString = window.atob(dataURI)
      const arrayBuffer = new ArrayBuffer(byteString.length)
      const int8Array = new Uint8Array(arrayBuffer)
      for (let i = 0; i < byteString.length; i++) {
        int8Array[i] = byteString.charCodeAt(i)
      }
      const blob = new Blob([int8Array], { type: 'application/pdf' })
      return blob
    },
    createUrl(path, data) {
      path = path + '?'
      for (const key of Object.keys(data)) {
        if (data[key] !== null) {
          if (path.at(-1) !== '?') {
            path = path + '&'
          }
          if (key === 'operator' || key === 'type') {
            path =
              path +
              key +
              '=' +
              (data[key]['_id']?.$oid
                ? data[key]['_id']['$oid']
                : data[key]['_id'])
          } else {
            path = path + key + '=' + data[key]
          }
        }
      }
      return path
    },
    exportPdf(type, title, download, loadingIndex, data) {
      if (download) {
        this.loadingExp[loadingIndex] = true
      } else {
        this.loadingShow[loadingIndex] = true
      }
      let path = '/exports/export/' + type
      path = this.createUrl(path, data)

      api
        .get(path)
        .then(response => {
          if (download) {
            const a = document.createElement('a')
            document.body.appendChild(a)
            const blob = this.dataURItoBlob(response.data.file)
            const url = URL.createObjectURL(blob)
            a.href = url
            a.download = title + '.pdf'
            a.click()
            setTimeout(() => {
              window.URL.revokeObjectURL(url)
              document.body.removeChild(a)
            }, 0)
            this.loadingExp[loadingIndex] = false
          } else {
            const blob = this.dataURItoBlob(response.data.file)
            const url = URL.createObjectURL(blob)
            // to open the PDF in a new window
            window.open(url, '_blank')
            this.loadingShow[loadingIndex] = false
          }
        })
        .catch(() => {
          this.showNotif('negative', "Impossibile eseguire l'export al momento")
          this.loadingExp[loadingIndex] = false
          this.loadingShow[loadingIndex] = false
        })
    },
    watchDate(value, field, variable) {
      if (
        value === null ||
        (field === 'end_date' && !this.validate(variable, value))
      ) {
        this[variable][field] = null
        return
      }
      this[variable][field] = value
    },
    watchMonthDate(value, reason, field) {
      if (value === null) {
        this[field].date = null
        return
      }
      if (reason === 'month') {
        this.$refs.monthPicker.hide()
      }
      this[field].date = value
    }
  }
}
</script>
<style></style>
