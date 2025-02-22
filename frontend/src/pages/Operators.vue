<template>
  <q-page class="q-mx-xl">
    <div class="row">
      <Heading :title="'Operatori'" />
    </div>
    <div class="row">
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
                isEdit = false
                dialog = true
              }
            ">
            Aggiungi Operatore</q-btn
          >
          <q-dialog v-model="dialog" persistent>
            <q-card>
              <q-card-section>
                <div class="text-h6">Aggiungi Operatore</div>
              </q-card-section>
              <q-form class="q-gutter-md">
                <q-card-section>
                  <q-input
                    v-model="operator.name"
                    outlined
                    class="q-mb-md"
                    label="Nome" />
                  <q-input
                    v-model="operator.surname"
                    outlined
                    class="q-my-md"
                    label="Cognome" />
                  <q-input
                    v-model="operator.username"
                    outlined
                    class="q-my-sm"
                    label="Username"
                    :rules="[
                      val =>
                        val.length > 6 ||
                        'Username deve contenere almeno 6 caratteri'
                    ]" />
                  <q-input
                    v-model="operator.email"
                    outlined
                    class="q-my-sm"
                    type="email"
                    label="Email"
                    style="text-transform: lowercase"
                    :rules="[val => !!val || 'Email mancante', isValidEmail]" />
                  <q-select
                    v-model="operator.role"
                    outlined
                    label="Ruolo"
                    :options="roles"
                    option-label="name"
                    emit-value
                    class="q-my-md"
                    ><template #no-option>
                      <q-item>
                        <q-item-section class="text-italic text-grey">
                          Nessun ruolo disponibile
                        </q-item-section>
                      </q-item>
                    </template></q-select
                  >
                  <q-input
                    v-model="operator.fiscal_code"
                    outlined
                    class="q-mt-md"
                    label="Codice Fiscale"
                    :rules="[isValidFiscalCode]"
                    style="text-transform: uppercase" />
                  <q-input
                    v-model="operator.hourly_cost"
                    outlined
                    class="q-mt-md"
                    label="Costo Orario" />
                </q-card-section>

                <q-card-section align="right" class="text-primary">
                  <q-btn
                    color="secondary"
                    :loading="loading"
                    style="width: 150px"
                    @click="isEdit ? save() : add()">
                    {{ isEdit ? 'Salva' : 'Aggiungi' }}
                    <template #loading>
                      <q-spinner-hourglass class="on-left" />
                      Loading...
                    </template>
                  </q-btn>
                  <q-btn
                    label="Cancella"
                    type="reset"
                    color="primary"
                    flat
                    class="q-ml-sm"
                    @click="reset()" />
                </q-card-section> </q-form
            ></q-card>
          </q-dialog>
        </template>
        <template #body-cell-role="props">
          <q-td :props="props">
            {{
              props.row?.role
                ? props.row.role.name + ' - ' + props.row.role.label
                : ''
            }}
          </q-td>
        </template>
        <template #body-cell-password="props">
          <q-td :props="props" class="pass_slot">
            <div>
              ********
              <q-icon name="edit" size="13px" class="q-mr-lg q-mb-sm" />
            </div>
            <q-popup-edit v-slot="{}" ref="popup" title="Cambio password">
              <div class="row">
                <q-input
                  v-model="password"
                  type="text"
                  dense
                  autofocus
                  :rules="[isValidPassword]"
                  @update:model-value="check($event)" />
              </div>
              <div class="row q-mt-lg q-ml-md">
                <q-btn
                  ref="close_popup"
                  v-close-popup
                  flat
                  color="primary"
                  @click="password = ''">
                  Cancella </q-btn
                ><q-btn
                  v-close-popup="close"
                  color="primary"
                  :disable="password === '' || password.trim() === ''"
                  @click="changePassword(props.row, password)">
                  Cambia
                </q-btn>
              </div>
            </q-popup-edit>
          </q-td>
        </template>
        <template #body-cell-actions="props">
          <q-td>
            <q-btn
              round
              icon="edit"
              color="green"
              size="sm"
              class="q-ml-lg"
              @click="editOperator(props.row)" />
            <q-btn
              round
              icon="delete"
              color="red"
              size="sm"
              class="q-ml-lg"
              @click="
                askConfirm(
                  'Sei sicuro di voler disattivare questo operatore',
                  deleteOperator,
                  props.row
                )
              " />
            <q-btn-dropdown
              flat
              round
              color="primary"
              icon="history"
              size="sm"
              :title="
                !props.row.reports || props.row.reports.length === 0
                  ? 'No reports available'
                  : 'View reports'
              ">
              <q-list>
                <q-item
                  v-for="report in props.row.reports"
                  :key="report._id"
                  v-close-popup
                  clickable
                  @click="viewReport(report._id)">
                  <q-item-section>
                    <div style="display: flex; flex-direction: column">
                      <span>{{
                        formatDateRange(report.pdf_selected_date_range)
                      }}</span>
                    </div>
                  </q-item-section>
                </q-item>
                <q-item v-if="props.row.reports.length === 0">
                  <q-item-section>
                    <span>No reports available</span>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
            <q-btn
              round
              icon="archive"
              color="orange"
              size="sm"
              class="q-ml-sm"
              :title="'Genera Report AI'"
              @click="generateReport(props.row)"
          /></q-td>
        </template>
        <template #no-data="{ message }">
          <div class="full-width row flex-center text-primary q-gutter-sm">
            <div v-if="message === 'Loading...'">{{ message }}</div>
            <div v-else>
              <q-icon size="2em" name="sentiment_dissatisfied" />
              <span>
                {{
                  errDataMsg
                    ? 'Impossibile caricare gli operatori al momento..'
                    : 'Nessun operatore presente ...'
                }}
              </span>
            </div>
          </div>
        </template>
        <template #body-cell-date_range="props">
          <q-td :props="props">
            <q-btn
              color="primary"
              label="Select Date Range"
              @click="openDateRangeDialog(props.row)" />
            <q-dialog v-model="props.row.showDateRangeDialog" persistent>
              <q-card style="min-width: 350px">
                <q-card-section>
                  <div class="text-h6">Select Date Range</div>
                </q-card-section>
                <q-card-section class="q-pt-none">
                  <q-date
                    v-model="props.row.dateRange"
                    range
                    emit-immediately />
                </q-card-section>
                <q-card-actions align="right" class="text-primary">
                  <q-btn v-close-popup flat label="Cancel" />
                  <q-btn
                    v-close-popup
                    flat
                    label="OK"
                    @click="saveDateRange(props.row)" />
                </q-card-actions>
              </q-card>
            </q-dialog>
          </q-td>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import Heading from 'components/Heading.vue'
import { useQuasar } from 'quasar'
import moment from 'moment'
import { api } from 'src/boot/axios'

export default {
  name: 'Operators',
  components: {
    Heading
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
      },
      showInsertedPassword(pass) {
        $q.dialog({
          title: 'Conferma',
          message:
            "La password assegnata all'utente è <strong>" +
            pass +
            "</strong>. \nSi prega di comunicare all'operatore la password al più presto.",
          ok: { push: true },
          persistent: true,
          html: true
        }).onDismiss(() => {
          this.password = ''
        })
      }
    }
  },
  data() {
    return {
      allReports: [],
      rows: [],
      columns: [
        {
          name: 'name',
          align: 'center',
          label: 'Nome',
          field: 'name',
          sortable: true
        },
        {
          name: 'surname',
          align: 'center',
          label: 'Cognome',
          field: 'surname',
          sortable: true
        },
        {
          name: 'username',
          align: 'center',
          label: 'Username',
          field: 'username',
          sortable: true
        },
        {
          name: 'role',
          align: 'center',
          label: 'Ruolo',
          field: 'role',
          sortable: true
        },
        {
          name: 'fiscal_code',
          align: 'center',
          label: 'Codice Fiscale',
          field: 'fiscal_code',
          sortable: true
        },
        {
          name: 'monthly_cost',
          align: 'center',
          label: 'Costo al Mese',
          field: 'monthly_cost',
          sortable: true
        },
        {
          name: 'email',
          align: 'center',
          label: 'Email',
          field: 'email',
          sortable: true
        },
        {
          name: 'password',
          align: 'center',
          label: 'Password',
          field: 'password',
          sortable: true
        },
        {
          name: 'actions',
          align: 'center',
          label: 'Azioni',
          sortable: true
        },
        {
          name: 'date_range',
          align: 'center',
          label: 'Date Range',
          field: 'date_range',
          sortable: false
        }
      ],
      loading: false,
      data_loading: true,
      errDataMsg: false,
      dialog: false,
      operator: {
        name: '',
        username: '',
        surname: '',
        email: '',
        role: null,
        fiscal_code: '',
        hourly_cost: '',
        monthly_cost: '',
        status: 'enabled',
        type: 'user'
      },
      pagination: {
        page: 0,
        rowsPerPage: 8
      },
      watchActive: false,
      password: '',
      isEdit: false,
      editedId: null,
      close: false,
      roles: []
    }
  },
  watch: {
    'operator.role': function (newRole) {
      if (this.watchActive && newRole && newRole.average_hour_cost) {
        this.operator.hourly_cost = newRole.average_hour_cost
      }
    }
  },
  mounted() {
    this.getOperators()
    this.getRoles()
    this.fetchAllReports()
  },
  methods: {
    fetchAllReports() {
      api
        .get('/tasks/operators/reports')
        .then(response => {
          this.allReports = response.data
          this.assignReportsToOperators()
        })
        .catch(error => {
          console.error('Error fetching reports:', error)
          this.showNotif('negative', 'Failed to fetch operator reports')
        })
    },
    assignReportsToOperators() {
      this.rows.forEach(operator => {
        operator.reports = this.allReports.filter(
          report => report.operator_id === operator._id.$oid
        )
      })
    },
    formatDateRange(range) {
      if (!range || typeof range !== 'object') {
        return 'Invalid date range'
      }

      const { start, end } = range

      if (!start || !end) {
        return 'Incomplete date range'
      }

      try {
        const startDate = moment(start).format('YYYY-MM-DD')
        const endDate = moment(end).format('YYYY-MM-DD')

        if (startDate === 'Invalid date' || endDate === 'Invalid date') {
          return 'Invalid date format'
        }

        return `${startDate} - ${endDate}`
      } catch (error) {
        console.error('Error formatting date range:', error)
        return 'Error in date range'
      }
    },
    getOperators() {
      api
        .get('/auth/user/operators?status=enabled')
        .then(response => {
          this.rows = response.data.map(row => ({
            ...row,
            dateRange: { from: null, to: null },
            showDateRangeDialog: false,
            reports: []
          }))
          this.assignReportsToOperators()
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
    getRoles() {
      api.get('/settings/setting/user/roles').then(response => {
        this.roles = response.data
      })
    },
    formatStrings(str) {
      const st = this.operator[str].toLowerCase()
      const toCapitalize = st.charAt(0).toUpperCase()
      this.operator[str] = toCapitalize + '' + st.slice(1)
    },
    openDateRangeDialog(row) {
      row.showDateRangeDialog = true
    },
    saveDateRange(row) {
      this.showNotif('positive', 'Date range saved successfully')
    },
    fetchReports(operator) {
      setTimeout(() => {
        operator.reports = [
          { id: 1, date: '2024-01-01' },
          { id: 2, date: '2024-02-01' },
          { id: 3, date: '2024-03-01' }
        ]
      }, 1000)
    },
    viewReport(reportId) {
      this.showNotif('info', `Opening report ${reportId}...`)

      api
        .get(`/reports/${reportId}`)
        .then(response => {
          const blob = this.dataURItoBlob(response.data)
          const url = URL.createObjectURL(blob)
          window.open(url, '_blank')
          this.showNotif('positive', 'Report opened successfully')
        })
        .catch(error => {
          console.error('Error opening report:', error)
          this.showNotif('negative', 'Failed to open report')
        })
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
    generateReport(operator) {
      if (!operator.dateRange.from || !operator.dateRange.to) {
        this.showNotif(
          'warning',
          `Please select a date range for ${operator.name} before generating a report.`
        )
        return
      }

      this.showNotif('info', `Generating report for ${operator.name}...`)

      const startDate = moment(operator.dateRange.from).format('YYYY-MM-DD')
      const endDate = moment(operator.dateRange.to).format('YYYY-MM-DD')
      const route = `/operators/${operator._id.$oid}/generate-report/${startDate}/${endDate}`

      api
        .get(route)
        .then(response => {
          if (response.data.success === false) {
            this.showNotif('negative', response.data.message)
            return
          }
          const newReport = {
            id: Date.now(),
            date: moment().format('YYYY-MM-DD')
          }
          if (!operator.reports) {
            operator.reports = []
          }
          this.fetchAllReports()
          this.showNotif('positive', `Report generated for ${operator.name}`)
        })
        .catch(error => {
          this.showNotif(
            'negative',
            `Failed to generate report for ${operator.name}`
          )
          console.error(error)
        })
    },
    addOperator() {
      this.formatStrings('name')
      this.formatStrings('surname')
      this.operator.fiscal_code = this.operator.fiscal_code.toUpperCase()
      const result = Object.assign({}, this.operator)
      result.role = this.operator.role._id
      api
        .post('/auth/user', result)
        .then(resp => {
          if (resp.data.success) {
            setTimeout(() => {
              this.loading = false
              this.showNotif('positive', 'Operatore caricato correttamente.')
              this.dialog = false
              this.reset()
            }, 500)
            api.post('/auth/log', {
              name: 'Aggiunta operatore : ' + this.operator.name,
              description: 'Operatore aggiunto correttamente',
              color: 'green'
            })
            this.getOperators()
            if (resp.data?.password) {
              this.showInsertedPassword(resp.data.password)
            }
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
              "L'operatore non è stato inserito correttamente."
            )
            this.dialog = false
            this.reset()
          }, 500)
        })
    },
    saveOperator() {
      this.formatStrings('name')
      this.formatStrings('surname')
      this.operator.fiscal_code = this.operator.fiscal_code.toUpperCase()
      const result = Object.assign({}, this.operator)
      result.role = this.operator.role._id.$oid
      api
        .put('/auth/user/edit/' + this.editedId, result)
        .then(resp => {
          if (resp.data.success) {
            setTimeout(() => {
              this.loading = false
              this.showNotif('positive', 'Operatore modificato correttamente')
              this.dialog = false
              this.editedId = null
              this.reset()
            }, 500)
            api.post('/auth/log', {
              name: 'Modifica operatore : ' + this.operator.name,
              description: 'Operatore modificato correttamente',
              color: 'green'
            })
            this.getOperators()
          } else if (resp.data?.msg) {
            setTimeout(() => {
              this.loading = false
              this.showNotif('warning', resp.data.msg)
            }, 500)
          }
        })
        .catch(error => {
          setTimeout(() => {
            this.loading = false
            this.showNotif(
              'negative',
              "L'operatore non è stato inserito correttamente."
            )
            this.dialog = false
            this.editedId = null
            this.reset()
          }, 500)
        })
    },
    check(e) {
      this.close = this.validatePassword(e) === null ? false : true
    },
    validateEmail(email) {
      return String(email)
        .toLowerCase()
        .match(
          /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/
        )
    },
    validateFiscalCode(fiscal_code) {
      return String(fiscal_code.toUpperCase()).match(
        /^([A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST]{1}[0-9LMNPQRSTUV]{2}[A-Z]{1}[0-9LMNPQRSTUV]{3}[A-Z]{1})$|([0-9]{11})$/
      )
    },
    validatePassword(password) {
      return String(password).match(/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/)
    },
    validate() {
      let isValid = true
      const fields = {
        name: 'Nome',
        surname: 'Cognome',
        username: 'Username',
        email: 'Email',
        role: 'Ruolo',
        fiscal_code: 'Codice fiscale',
        hourly_cost: 'Costo orario'
      }
      for (const [key, value] of Object.entries(this.operator)) {
        if (
          (typeof value === 'object' && value.length === 0) ||
          (typeof value === 'string' &&
            (value === '' || value.trim() === '')) ||
          value === undefined
        ) {
          this.showNotif(
            'warning',
            'Il campo ' + fields[key] + ' deve essere inserito.'
          )
          isValid = false
        } else if (key === 'email' && this.validateEmail(value) === null) {
          this.showNotif('warning', "L'email inserita non è valida.")
          isValid = false
        } else if (key === 'username' && value.length < 6) {
          this.showNotif(
            'warning',
            "L'username deve contenere almeno 6 caratteri"
          )
          isValid = false
        } else if (
          key === 'fiscal_code' &&
          this.validateFiscalCode(value) === null
        ) {
          this.showNotif('warning', 'Il codice fiscale inserito non è valido.')
          isValid = false
        }
      }
      return isValid
    },
    save() {
      if (this.validate()) {
        this.loading = true
        this.saveOperator()
      }
    },
    add() {
      if (this.validate()) {
        this.loading = true
        this.addOperator()
      }
    },
    changePassword(row, password) {
      if (this.validatePassword(password)) {
        api
          .put('/auth/user/change-password/' + row._id.$oid, {
            password: password
          })
          .then(resp => {
            this.showNotif('positive', 'Password modificata con successo')
            if (resp.data?.password) {
              this.showInsertedPassword(resp.data.password)
            }
          })
          .catch(er => {
            this.showNotif(
              'negative',
              'Impossibile modificare la password al momento'
            )
          })
      } else {
        this.showNotif('warning', 'Password non valida.')
      }
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
    deleteOperator(row) {
      api
        .put('/auth/user/' + row._id.$oid)
        .then(resp => {
          if (resp.data.success) {
            this.showNotif('positive', 'Operatore eliminato correttamente')
            api.post('/auth/log', {
              name: 'Eliminazione operatore : ' + row.name + ' ' + row.surname,
              description: 'Operatore eliminato correttamente',
              color: 'green'
            })
            this.getOperators()
          } else {
            this.showNotif(
              'negative',
              "Errore durante l'eliminazione dell'operatore"
            )
          }
        })
        .catch(error => {
          this.showNotif(
            'negative',
            "Errore durante l'eliminazione dell'operatore"
          )
        })
    },
    editOperator(row) {
      this.dialog = true
      this.editedId = row._id.$oid
      this.operator = {
        name: row.name,
        surname: row.surname,
        username: row.username,
        email: row.email,
        role: row.role,
        fiscal_code: row.fiscal_code,
        status: 'enabled',
        type: 'user',
        hourly_cost: row.hourly_cost
      }
      this.watchActive = false // Disable the watch
      this.$nextTick(() => {
        this.watchActive = true // Enable the watch after the next DOM update cycle
      })
      this.isEdit = true
    },
    reset() {
      this.dialog = false
      this.operator = {
        name: '',
        surname: '',
        username: '',
        email: '',
        role: '',
        fiscal_code: '',
        hourly_cost: '',
        status: 'enabled',
        type: 'user'
      }
    },
    isValidEmail(val) {
      const emailPattern =
        /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/
      return emailPattern.test(val) || 'Email non valida'
    },
    isValidPassword(val) {
      const passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/
      return (
        passwordPattern.test(val) ||
        'La password deve essere di almeno 8 caratteri: Deve contenere: \n\n una lettera maiuscola, una lettera minuscola e almeno un numero.'
      )
    },
    isValidFiscalCode(val) {
      const fiscalPattern =
        /^([A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST]{1}[0-9LMNPQRSTUV]{2}[A-Z]{1}[0-9LMNPQRSTUV]{3}[A-Z]{1})$|([0-9]{11})$/
      return (
        fiscalPattern.test(val.toUpperCase()) || 'Codice fiscale non valido'
      )
    }
  }
}
</script>
<style scoped>
.q-table__container.q-table--horizontal-separator.column.no-wrap.q-table__card.q-table--no-wrap {
  width: 98%;
  margin-left: 10px;
}

.q-field--outlined .q-field__control {
  margin: 10px;
}

.pass_slot {
  cursor: pointer;
}
</style>
