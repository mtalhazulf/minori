<template>
  <q-page class="q-mx-xl">
    <div class="row">
      <div class="col-10">
        <Heading :title="'Registro presenze minori'" />
      </div>
      <div v-if="operator.usertype === 'user'" class="col">
        <q-btn
          color="secondary"
          label="Aggiungi minore"
          style="width: 180px"
          class="q-mr-md"
          @click="
            () => {
              reset()
              isEdit = false
              dialog = true
            }
          " />

        <q-dialog v-model="dialog">
          <q-card>
            <q-card-section>
              <div class="text-h6">Nuovo minore</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              <form class="q-my-sm">
                <q-input
                  v-model="minor.name"
                  outlined
                  label="Nome"
                  class="q-my-sm" />
                <q-input
                  v-model="minor.surname"
                  outlined
                  label="Cognome"
                  class="q-my-sm" />
                <q-input
                  v-model="minor.fiscal_code"
                  outlined
                  label="Codice Fiscale"
                  :rules="[isValidFiscalCode]"
                  style="text-transform: uppercase"
                  class="q-my-sm" />
              </form>
            </q-card-section>

            <q-card-actions align="right">
              <q-btn
                v-close-popup
                flat
                label="Cancella"
                color="primary"
                @click="reset()" />
              <q-btn
                :label="isEdit ? 'Salva' : 'Aggiungi'"
                color="primary"
                :disable="!validate()"
                @click="isEdit ? editMinor() : addMinor()" />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </div>
    </div>
    <div class="row">
      <q-table
        v-model:pagination="pagination"
        :rows="rows"
        :columns="columns"
        row-key="id"
        :loading="data_loading"
        :rows-per-page-options="[5, 8, 10, 15, 25, 50]">
        <template #top>
          <q-space />
          <div
            v-if="
              operator.usertype === 'admin' ||
              operator.usertype === 'superadmin'
            "
            class="row">
            <div class="col">
              <q-btn
                color="primary"
                icon="chevron_left"
                class="q-mr-md"
                @click="prev()" />
            </div>
            <div class="col-9 cursor-pointer q-px-lg">
              {{ convertDate(today) }}
              <q-popup-edit v-slot="scope" v-model="today" auto-save>
                <q-date
                  v-model="scope.value"
                  minimal
                  :options="optionsFn"
                  @update:model-value="scope.set" />
              </q-popup-edit>
            </div>
            <div class="col">
              <q-btn
                v-if="!checkDate()"
                color="primary"
                icon="navigate_next"
                class="q-ml-md"
                @click="next()" />
            </div>
          </div>
          <q-space />
          <q-btn
            color="secondary"
            :loading="loading"
            style="width: 150px"
            :disable="!checkDate() || rows.length === 0"
            @click="save()">
            Salva presenze
            <template #loading>
              <q-spinner-hourglass class="on-left" />
              Loading...
            </template>
          </q-btn>
        </template>
        <template #body-cell-isPresent="props">
          <q-td :props="props">
            <div v-if="checkDate()">
              <q-checkbox v-model="props.row.isPresent" dense />
            </div>
            <div v-else>
              <q-icon
                :name="props.row.isPresent ? 'done' : 'close'"
                size="sm"
                :color="props.row.isPresent ? 'green' : 'red'" />
            </div>
          </q-td>
        </template>

        <template #no-data="{ message }">
          <div class="full-width row flex-center text-primary q-gutter-sm">
            <div v-if="message === 'Loading...'">{{ message }}</div>
            <div v-else>
              <q-icon size="2em" name="sentiment_dissatisfied" />
              <span>
                {{
                  errDataMsg
                    ? 'Impossibile caricare le presenze al momento..'
                    : 'Nessuna presenza presente ...'
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
import { useQuasar } from 'quasar'
import moment from 'moment'
import { api } from 'src/boot/axios'

export default {
  name: 'MinorAttendanceRegister',
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
          timeout: 1500
        })
      },
      optionsFn(date) {
        return new Date(date) <= new Date()
      }
    }
  },
  data() {
    return {
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
          name: 'isPresent',
          align: 'center',
          label: 'Presenza',
          field: 'isPresent',
          sortable: true
        }
      ],
      loading: false,
      data_loading: true,
      dialog: false,
      editedId: null,
      isEdit: false,
      minor: {
        name: '',
        surname: '',
        fiscal_code: ''
      },
      operator: '',
      today: new Date(),
      errDataMsg: false,
      pagination: {
        page: 0,
        rowsPerPage: 8
      }
    }
  },
  watch: {
    today(e, n) {
      this.getPresences()
    }
  },
  mounted() {
    this.operator = JSON.parse(sessionStorage.getItem('user'))
    this.today = moment(String(this.today)).format('YYYY/MM/DD')
    this.getPresences(this.today)
  },
  methods: {
    getPresences() {
      api
        .get('/minors/attendance', {
          params: { current_date: this.today }
        })
        .then(response => {
          if (response.data.length > 0) {
            this.rows = response.data
            setTimeout(() => {
              this.errDataMsg = false
              this.data_loading = false
            }, 500)
          } else {
            if (this.checkDate()) {
              this.getMinors()
            } else {
              this.rows = []
            }
          }
        })
        .catch(() => {
          this.errDataMsg = true
          this.data_loading = false
        })
    },
    getMinors() {
      api
        .get('/minors/minor/all')
        .then(response => {
          this.rows = response.data.map(v => ({ ...v, isPresent: false }))
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
    formatStrings(str) {
      const st = this.minor[str].toLowerCase()
      const toCapitalize = st.charAt(0).toUpperCase()
      this.minor[str] = toCapitalize + '' + st.slice(1)
    },
    save() {
      this.loading = true
      const result = this.rows.map(x => {
        return { _id: x._id, isPresent: x.isPresent }
      })
      api
        .post('/minors/attendance', result)
        .then(resp => {
          this.loading = false
          const msg = 'Presenze/Assenze caricate correttamente'
          this.showNotif('positive', msg)
          const operatorName = JSON.parse(sessionStorage.getItem('user')).name

          api.post('/auth/log', {
            name: 'Compilazione registro',
            description: 'Registro minori modificato correttamente',
            color: 'green'
          })
          this.getPresences(this.today)
        })
        .catch(er => {
          this.loading = false
          this.showNotif(
            'negative',
            'Errore durante il salvataggio delle presenze'
          )
        })
    },
    validate() {
      if (
        this.minor.name === '' ||
        this.minor.name.trim() === '' ||
        this.minor.surname === '' ||
        this.minor.surname.trim() === ''
      ) {
        return false
      } else {
        if (
          this.minor.fiscal_code !== undefined &&
          this.minor.fiscal_code.length > 0
        ) {
          if (this.validateFiscalCode(this.minor.fiscal_code) === null) {
            return false
          } else {
            this.minor.fiscal_code = this.minor.fiscal_code.toUpperCase()
          }
        }
        return true
      }
    },
    validateFiscalCode(fiscal_code) {
      return String(fiscal_code.toUpperCase()).match(
        /^([A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST]{1}[0-9LMNPQRSTUV]{2}[A-Z]{1}[0-9LMNPQRSTUV]{3}[A-Z]{1})$|([0-9]{11})$/
      )
    },
    addMinor() {
      if (this.validate()) {
        this.formatStrings('name')
        this.formatStrings('surname')
        api
          .post('/minors/minor', this.minor)
          .then(response => {
            if (response.data.success) {
              const msg = 'Minore aggiunto correttamente!'
              this.showNotif('positive', msg)
              api.post('/auth/log', {
                name:
                  'Aggiunta minore : ' +
                  this.minor.name +
                  ' ' +
                  this.minor.surname,
                description: 'Minore aggiunto correttamente',
                color: 'green'
              })
              this.dialog = false
              this.getPresences(this.today)
            } else if (!response.data.success && response.data?.msg) {
              this.showNotif('warning', response.data.msg)
            } else {
              this.showNotif('negative', "Errore durante l'aggiunta del minore")
            }
          })
          .catch(er => {
            this.showNotif('negative', "Errore durante l'aggiunta del minore")
            this.dialog = false
          })
      }
    },
    editMinor() {
      if (this.validate()) {
        this.formatStrings('name')
        this.formatStrings('surname')
        api
          .put('/minors/minor/' + this.editedId, this.minor)
          .then(resp => {
            if (resp.data.success) {
              this.showNotif('positive', 'Minore modificato correttamente')
              api.post('/auth/log', {
                name:
                  'Modifica minore : ' +
                  this.minor.name +
                  ' ' +
                  this.minor.surname,
                description: 'Minore modificato correttamente',
                color: 'green'
              })
              this.dialog = false
              this.editedId = null
              this.today = moment(String(this.today)).format('YYYY/MM/DD')
              this.getPresences(this.today)
            } else if (resp.data?.msg) {
              this.showNotif('warning', resp.data.msg)
            } else {
              this.showNotif(
                'negative',
                'Errore durante la modifica del minore'
              )
            }
          })
          .catch(error => {
            this.showNotif('negative', 'Errore durante la modifica del minore')
            this.dialog = false
            this.editedId = null
          })
      }
    },
    convertDate(date) {
      return moment(String(date)).lang('it').format('dddd DD MMMM')
    },
    prev() {
      const curr_date = new Date(moment(this.today).subtract(1, 'days'))
      this.today = moment(String(curr_date)).format('YYYY/MM/DD')
    },
    next() {
      const curr_date = new Date(moment(this.today).add(1, 'days'))
      this.today = moment(String(curr_date)).format('YYYY/MM/DD')
    },
    checkDate() {
      return moment(moment(this.today).startOf('day')).isSame(
        moment(new Date()).startOf('day')
      )
    },
    reset() {
      this.dialog = false
      this.minor = { name: '', surname: '', fiscal_code: '' }
    },
    isValidFiscalCode(val) {
      const fiscalPattern =
        /^([A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST]{1}[0-9LMNPQRSTUV]{2}[A-Z]{1}[0-9LMNPQRSTUV]{3}[A-Z]{1})$|([0-9]{11})$/
      if (val.trim().length === 0) {
        return true
      } else {
        return (
          fiscalPattern.test(val.toUpperCase()) || 'Codice fiscale non valido'
        )
      }
    }
  }
}
</script>
<style scoped>
.q-table__container.q-table--horizontal-separator.column.no-wrap.q-table__card.q-table--no-wrap {
  width: 98%;
  margin-left: 10px;
}

.col {
  display: flex;
  align-items: center;
  justify-content: end;
}
.q-menu.q-position-engine.scroll.q-popup-edit {
  padding: 0 !important;
}
</style>
