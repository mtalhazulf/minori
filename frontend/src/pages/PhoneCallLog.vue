<template>
  <q-page>
    <div class="row q-mx-xl">
      <Heading :title="'Registro telefonate'" />
    </div>
    <div class="row q-ml-lg q-mr-sm">
      <q-expansion-item
        id="expansioned_item"
        v-model="expanded"
        label="Filtri"
        class="q-mx-md q-ml-lg">
        <q-separator />
        <q-card>
          <q-card-section>
            <div class="row">
              <q-select
                v-model="filters.minor"
                outlined
                class="q-ma-md"
                label="Ospite"
                :options="minors.length === 0 ? [] : minors"
                :option-label="opt => opt.name + ' ' + opt.surname"
                emit-value
                style="width: 20%"
                ><template #no-option>
                  <q-item>
                    <q-item-section class="text-italic text-grey">
                      Nessun ospite disponibile
                    </q-item-section>
                  </q-item>
                </template></q-select
              >
              <q-select
                v-model="filters.operator"
                outlined
                class="q-ma-md"
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
              <q-input
                v-model="filters.date"
                outlined
                class="q-ma-md"
                label="Data: "
                readonly
                style="background: white; width: 190px">
                <template #append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy
                      ref="qDateProxy"
                      cover
                      transition-show="scale"
                      transition-hide="scale">
                      <q-date
                        type="date"
                        @update:model-value="
                          (value, reason, detail) => {
                            watchFilterDate(value, reason, detail)
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
            <div class="row d-flex justify-end">
              <q-btn
                label="Applica filtri"
                icon="filter_alt"
                class="q-mt-lg q-mx-sm"
                color="green"
                style="height: 10px"
                @click="applyFilters()" />
              <q-btn
                icon="filter_alt_off"
                label="Rimuovi filtri"
                class="q-mt-lg q-mx-sm text-black"
                color="standard"
                style="height: 10px"
                @click="resetFilters()" />
            </div>
          </q-card-section>
        </q-card>
      </q-expansion-item>
    </div>
    <div class="row q-ml-lg q-pl-lg justify-start q-mb-md">
      <q-table
        v-model:pagination="pagination"
        :rows="rows"
        :columns="columns"
        row-key="id"
        :loading="data_loading"
        :rows-per-page-options="[5, 8, 10, 15, 25, 50]"
        @request="onRequest">
        <template #top-right>
          <q-btn
            color="secondary"
            style="width: 150px"
            @click="
              () => {
                reset()
                isEdit = false
                dialog = true
              }
            ">
            Aggiungi Telefonata</q-btn
          >
          <q-dialog v-model="dialog" persistent>
            <q-card>
              <q-card-section>
                <div class="text-h6">
                  {{ isEdit ? 'Modifica telefonata' : 'Aggiungi telefonata' }}
                </div>
              </q-card-section>
              <q-card-section class="q-pt-none">
                <q-form class="q-my-sm">
                  <q-card-section>
                    <q-select
                      ref="selectMinor"
                      v-model="call.minors"
                      outlined
                      multiple
                      :options="minors"
                      label="Ospiti"
                      use-chips
                      emit-value
                      map-options
                      class="q-my-md"
                      :option-label="opt => opt.name + ' ' + opt.surname"
                      :option-value="opt => opt._id.$oid"
                      @update:model-value="close('selectMinor')">
                      <template #no-option>
                        <q-item>
                          <q-item-section class="text-italic text-grey">
                            Non sono presenti ospiti
                          </q-item-section>
                        </q-item>
                      </template>
                    </q-select>
                    <q-input
                      v-model="call.date"
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
                      v-model="call.hour"
                      outlined
                      mask="time"
                      :rules="['time']"
                      class="q-mt-sm"
                      label="Inserisci Ora: "
                      readonly>
                      <template #append>
                        <q-icon name="access_time" class="cursor-pointer">
                          <q-popup-proxy
                            cover
                            transition-show="scale"
                            transition-hide="scale">
                            <q-time
                              v-model="call.hour"
                              format24h
                              :options="
                                (hour, minute) =>
                                  optionsTime(call.date, hour, minute)
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
                    <q-input
                      v-model="call.phone_call_issuer"
                      class="q-mb-md"
                      outlined
                      label="Emittente telefonata" />
                    <q-input
                      v-model="call.notes"
                      outlined
                      type="textarea"
                      label="Note" />
                  </q-card-section>
                </q-form>
              </q-card-section>

              <q-card-section align="right" class="text-primary">
                <q-btn
                  color="secondary"
                  :loading="loading"
                  style="width: 150px"
                  @click="isEdit ? editCall() : add()">
                  Salva
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
            <q-td key="date" :props="props">{{
              convertDate(props.row.date)
            }}</q-td>
            <q-td key="date" :props="props">
              {{ convertHours(props.row.date) }}</q-td
            >
            <q-td key="minors" :props="props">
              <div v-for="(minor, key) in props.row.minors" :key="minor._id">
                {{ minor.name + ' ' + minor.surname }}
                <span v-if="key + 1 != props.row.minors.length">, </span>
              </div>
            </q-td>
            <q-td key="phone_call_issuer" :props="props">{{
              props.row.phone_call_issuer
            }}</q-td>
            <q-td key="notes" :props="props">
              <div v-if="props.row.notes.length > 60">
                <div>{{ props.row.notes.substring(0, 60) + '...' }}</div>
                <q-tooltip max-width="30%"> {{ props.row.notes }} </q-tooltip>
              </div>
              <div v-else>{{ props.row.notes }}</div></q-td
            >

            <q-td key="operator" :props="props">{{
              props.row.operator?.name
                ? props.row.operator.name + ' ' + props.row.operator.surname
                : props.row.operator.companyName
            }}</q-td>
            <q-td key="actions" :props="props"
              ><q-btn
                round
                icon="edit"
                color="green"
                size="sm"
                @click="edit(props.row)" />
              <q-btn
                round
                icon="delete"
                color="red"
                size="sm"
                class="q-ml-lg"
                @click="
                  askConfirm(
                    'Sei sicuro di voler eliminare la telefonata?',
                    deleteCall,
                    props.row
                  )
                "
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
                    ? 'Impossibile caricare le telefonate effettuate al momento..'
                    : 'Nessuna telefonata presente ...'
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
import moment from 'moment'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'
import { date } from 'quasar'

export default {
  name: 'PhoneCallLog',
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
          name: 'date',
          required: true,
          label: 'Data',
          align: 'center',
          field: 'date'
        },
        {
          name: 'date',
          required: true,
          label: 'Ora',
          align: 'center',
          field: 'date'
        },
        {
          name: 'minors',
          align: 'center',
          label: 'Ospite destinatario',
          field: 'minors',
          sortable: true
        },
        {
          name: 'phone_call_issuer',
          align: 'center',
          label: ' Emittente telefonata',
          field: 'phone_call_issuer'
        },
        {
          name: 'notes',
          align: 'center',
          label: ' Note',
          field: 'notes'
        },
        {
          name: 'operator',
          align: 'center',
          label: ' Operatore',
          field: 'operator'
        },
        {
          name: 'actions',
          align: 'center',
          label: ' Azioni',
          field: 'actions'
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
      minors: [],
      call: {
        date: null,
        hour: null,
        minors: [],
        phone_call_issuer: '',
        notes: ''
      },
      isEdit: false,
      editedId: null,
      filters: {
        minor: null,
        operator: null,
        date: null
      },
      expanded: false,
      operators: []
    }
  },
  mounted() {
    this.getCallLogs()
    this.getMinors()
    this.getOperators()
  },
  methods: {
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
    onRequest(props) {
      const { page, rowsPerPage } = props.pagination
      this.pagination.page = page
      this.pagination.rowsPerPage = rowsPerPage
      this.getCallLogs()
    },
    getCallLogs(url = '') {
      let path =
        '/tasks/calls?page=' +
        (this.pagination.page - 1) +
        '&limit=' +
        this.pagination.rowsPerPage
      if (url.trim() !== '') {
        path += url
      }
      api
        .get(path)
        .then(resp => {
          if (!Array.isArray(resp.data)) {
            this.rows = resp.data.paginatedResults
            this.pagination = resp.data.meta
          } else {
            this.rows = []
          }
          setTimeout(() => {
            this.errDataMsg = false
            this.data_loading = false
          }, 500)
        })
        .catch(() => {
          this.rows = []
          this.errDataMsg = true
          this.data_loading = false
        })
    },
    getMinors() {
      api.get('/minors/minor/all').then(response => {
        this.minors = response.data
      })
    },
    getOperators() {
      api
        .get('/auth/user/operators')
        .then(response => {
          this.operators = response.data
        })
        .catch(() => {
          this.operators = []
        })
    },
    watchDate(value, reason, detail) {
      this.call.date = moment(value).format('DD/MM/YYYY')
    },
    reset() {
      this.call = {
        date: null,
        hour: null,
        minors: [],
        phone_call_issuer: '',
        notes: ''
      }
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

      if (this.call.minors.length === 0) {
        isValid = false
        this.showNotif('warning', 'Inserire ospite')
      }
      if (this.call.date === null) {
        isValid = false
        this.showNotif('warning', 'Inserire data')
      }
      if (this.call.hour === null) {
        isValid = false
        this.showNotif('warning', 'Inserire ora')
      }
      if (this.call.phone_call_issuer.trim() === '') {
        isValid = false
        this.showNotif('warning', 'Inserire emittente telefonata')
      }

      return isValid
    },
    add() {
      if (this.validate()) {
        const result = Object.assign({}, this.call)
        result.date = `${result.date} ${result.hour}:00`
        delete result.hour
        this.loading = true
        api
          .post('/tasks/calls', result)
          .then(resp => {
            if (resp.data.success) {
              setTimeout(() => {
                this.loading = false
                this.showNotif('positive', 'Telefonata caricata correttamente.')
                this.dialog = false
                this.reset()
              }, 500)

              this.getCallLogs()
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
                'La telefonata non è stata inserita correttamente.'
              )
              this.dialog = false
              this.reset()
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
      return moment(String(date)).format('DD/MM/YYYY')
    },
    convertHours(date) {
      if (date) {
        return moment(String(date)).format('HH:mm')
      } else {
        return true
      }
    },

    close(ref) {
      this.$refs[ref].hidePopup()
    },
    edit(row) {
      this.dialog = true
      this.editedId = row._id.$oid
      this.call = {
        date: this.convertDate(row.date),
        hour: this.convertHours(row.date),
        minors: row.minors.map(x => {
          return x._id.$oid
        }),
        phone_call_issuer: row.phone_call_issuer,
        notes: row.notes
      }
      this.isEdit = true
    },
    editCall() {
      if (this.validate()) {
        const result = Object.assign({}, this.call)
        result.date = `${result.date} ${result.hour}:00`
        delete result.hour
        this.loading = true

        api
          .put('/tasks/calls/' + this.editedId, result)
          .then(resp => {
            setTimeout(() => {
              this.loading = false
              this.showNotif('positive', 'Telefonata modificata correttamente.')
              this.dialog = false
              this.reset()
            }, 500)
            this.getCallLogs()
          })
          .catch(error => {
            setTimeout(() => {
              this.loading = false
              this.showNotif(
                'negative',
                'La telefonata non è stata modificata correttamente.'
              )
              this.dialog = false
              this.reset()
            }, 500)
          })
      }
    },
    deleteCall(row) {
      api
        .delete('/tasks/calls/' + row._id.$oid)
        .then(resp => {
          if (resp.data.success) {
            this.showNotif('positive', 'Telefonata eliminata correttamente.')
            this.getCallLogs()
          } else {
            this.showNotif(
              'negative',
              "Errore durante l'eliminazione della telefonata."
            )
          }
        })
        .catch(error => {
          this.showNotif(
            'negative',
            "Errore durante l'eliminazione della telefonata."
          )
        })
    },
    watchFilterDate(value, reason, detail) {
      this.filters.date = moment(value).format('DD/MM/YYYY')
    },
    addFilters(url) {
      Object.keys(this.filters).forEach(el => {
        if (typeof this.filters[el] === 'string') {
          if (this.filters[el].trim() !== '') {
            url += '&' + el + '=' + this.filters[el].toLowerCase()
          }
        } else if (typeof this.filters[el] === 'object') {
          if (this.filters[el] !== null) {
            url += '&' + el + '=' + this.filters[el]._id.$oid
          }
        }
      })
      return url
    },
    applyFilters() {
      let url = ''
      url = this.addFilters(url)
      if (url !== '') {
        this.getCallLogs(url, 0)
      } else {
        this.showNotif('info', 'Non è stato inserito alcun filtro')
      }
    },
    resetFilters() {
      this.expanded = false

      this.filters = {
        minor: null,
        operator: null,
        date: null
      }
      this.getCallLogs()
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

#expansioned_item {
  width: 100%;
  background: white;
  box-shadow: rgb(0 0 0 / 20%) 0px 1px 5px, rgb(0 0 0 / 14%) 0px 2px 2px,
    rgb(0 0 0 / 12%) 0px 3px 1px -2px;
  border-radius: 5px;
  margin-bottom: 10px;
}
</style>
