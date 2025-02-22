<template>
  <q-page class="q-mx-xl">
    <div class="row"><Heading :title="'Fascicolo Minori'" /></div>
    <div class="row">
      <q-expansion-item
        id="expansioned_item"
        v-model="expanded"
        label="Filtri"
        class="q-mx-sm">
        <q-separator />
        <q-card>
          <q-card-section>
            <div class="row">
              <q-input
                v-model="filters.name"
                outlined
                class="q-ma-md"
                label="Nome"
                style="background: white; width: 190px" /><q-input
                v-model="filters.surname"
                outlined
                class="q-ma-md"
                label="Cognome"
                style="background: white; width: 190px" />
              <q-input
                v-model="filters.fiscal_code"
                outlined
                class="q-ma-md"
                label="Codice fiscale"
                style="background: white; width: 190px" />
              <q-input
                v-model="filters.entry_date"
                outlined
                class="q-ma-md"
                label="Ammessi dopo: "
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
    <div class="row q-mb-md">
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
        </template>
        <template #body-cell-admission_date="props">
          <q-td style="text-align: center">
            {{ props.row.info_sheet?.minor?.entry_date ?? '' }}
          </q-td>
        </template>
        <template #body-cell-dismission_date="props">
          <q-td style="text-align: center">
            {{ props.row.info_sheet?.minor?.disposal_date ?? '' }}
          </q-td>
        </template>
        <template #body-cell-importo="props">
          <q-td style="text-align: center">
            {{
              props.row.info_sheet?.minor?.amount_euro
                ? props.row.info_sheet.minor.amount_euro + ' €'
                : ''
            }}
          </q-td>
        </template>
        <template #body-cell-actions="props">
          <q-td
            style="display: flex; justify-content: center; align-items: center">
            <q-btn-dropdown
              :disabled="filteredMinors[props.row._id.$oid] === undefined"
              icon="history"
              :title="
                filteredMinors[props.row._id.$oid] === undefined
                  ? `Nessuna scheda archiviata`
                  : `Visualizza schede PDF archiviate`
              ">
              <q-list>
                <q-item
                  v-for="archive in filteredMinors[props.row._id.$oid]"
                  :key="archive._id"
                  v-close-popup
                  title="Visualizza scheda PDF archiviata"
                  clickable
                  @click="viewArchive(archive._id)">
                  <q-item-section>
                    <div style="display: flex; align-items: center">
                      <q-icon name="event" class="q-mr-sm" />
                      <span>
                        {{
                          new Date(archive.archive_date).toLocaleDateString(
                            'it-IT',
                            { day: 'numeric', month: 'long', year: 'numeric' }
                          )
                        }}
                      </span>
                    </div>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
            <q-btn
              round
              icon="archive"
              color="orange"
              size="sm"
              class="q-ml-lg"
              :title="
                !props.row.info_sheet?.semestral_comunication.date
                  ? `Impossibile archiviare, data scheda mancante
              `
                  : `Genera scheda semestrale`
              "
              :disable="!props.row.info_sheet?.semestral_comunication.date"
              @click="
                askConfirm(
                  'Sei sicuro di voler generare la scheda semestrale per questo minore? Questa operazione è irreversibile e non sarà possibile effettuare modifiche.',
                  archiveMinor,
                  props.row
                )
              " />
            <q-btn
              round
              icon="smart_toy"
              color="teal"
              size="sm"
              class="q-ml-lg"
              :title="'Genera PDF Valutazione AI'"
              :disable="!props.row.info_sheet?.semestral_comunication.date"
              @click="viewAIReport(props.row)" />
            <q-btn
              round
              icon="visibility"
              color="blue"
              size="sm"
              class="q-ml-lg"
              :title="`Visualizza scheda PDF minore`"
              @click="view(props.row)" />
            <q-btn
              round
              icon="edit"
              color="green"
              size="sm"
              class="q-ml-lg"
              :title="`Modifica minore`"
              @click="edit(props.row)" />
            <q-btn
              round
              icon="menu_book"
              color="purple"
              size="sm"
              class="q-ml-lg"
              :title="`Modifica scheda PDF minore`"
              @click="editFile(props.row)" />
            <q-btn
              round
              icon="delete"
              color="red"
              size="sm"
              class="q-ml-lg"
              :title="`Elimina minore`"
              @click="
                askConfirm(
                  'Sei sicuro di voler eliminare questo minore?',
                  deleteMinor,
                  props.row
                )
              "
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
                    ? 'Impossibile caricare i minori al momento..'
                    : 'Nessun minore presente ...'
                }}
              </span>
            </div>
          </div>
        </template>

        <q-btn
          v-if="scope.pagesNumber > 2"
          icon="first_page"
          color="grey-8"
          round
          dense
          flat
          :disable="scope.isFirstPage"
          @click="getMinors()" />

        <q-btn
          icon="chevron_left"
          color="grey-8"
          round
          dense
          flat
          :disable="scope.isFirstPage"
          @click="getMinors('', scope.pagination.page - 2)" />
        {{ scope.pagination.page }}/{{ scope.pagesNumber }}
        <q-btn
          icon="chevron_right"
          color="grey-8"
          round
          dense
          flat
          :disable="scope.isLastPage"
          @click="getMinors('', scope.pagination.page)" />

        <q-btn
          v-if="scope.pagesNumber > 2"
          icon="last_page"
          color="grey-8"
          round
          dense
          flat
          :disable="scope.isLastPage"
          @click="getMinors('', scope.pagesNumber)" />
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
  name: 'Minors',
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
          field: 'name'
        },
        {
          name: 'surname',
          align: 'center',
          label: 'Cognome',
          field: 'surname'
        },
        {
          name: 'fiscal_code',
          align: 'center',
          label: 'Codice Fiscale',
          field: 'fiscal_code'
        },
        {
          name: 'admission_date',
          align: 'center',
          label: 'Data ammissione'
        },
        {
          name: 'dismission_date',
          align: 'center',
          label: 'Data dismissione'
        },
        {
          name: 'importo',
          align: 'center',
          label: 'Importo'
        },
        {
          name: 'actions',
          align: 'center',
          label: 'Azioni'
        }
      ],
      loading: false,
      data_loading: true,
      errDataMsg: false,
      dialog: false,
      minor: {
        name: '',
        surname: '',
        fiscal_code: ''
      },
      pagination: {
        page: 0,
        rowsPerPage: 8
      },
      isEdit: false,
      editedId: null,
      filters: {
        name: '',
        surname: '',
        fiscal_code: '',
        entry_date: null
      },
      expanded: false,
      minorArchives: []
    }
  },
  computed: {
    filteredMinors() {
      const filtered = {}
      this.rows.forEach(minor => {
        const filteredMinors = this.minorArchives.filter(
          archive => archive.id_children === minor._id.$oid
        )
        if (filteredMinors.length > 0) {
          filtered[minor._id.$oid] = filteredMinors
        }
      })
      return filtered
    }
  },
  mounted() {
    this.getMinors()
    this.fetchMinorArchives()
  },
  methods: {
    onRequest(props) {
      const { page, rowsPerPage } = props.pagination
      this.pagination.page = page
      this.pagination.rowsPerPage = rowsPerPage
      this.getMinors()
    },

    fetchMinorArchives() {
      api
        .get('/exports/archive/minor')
        .then(r => {
          this.minorArchives = r.data
        })
        .catch(() => {
          this.showNotif(
            'negative',
            "Errore durante lo scaricamento dell'archivio minori"
          )
        })
    },

    archiveMinor(row) {
      if (!row.info_sheet.semestral_comunication.date) {
        this.showNotif(
          'negative',
          'Impossibile archiviare il minore, data nel fascicolo assente'
        )
        return
      }
      api
        .post('/exports/archive/minor/' + row._id.$oid)
        .then(r => {
          if (r.data.success) {
            this.showNotif('positive', 'Minore archiviato con successo')
            this.getMinors()
            this.fetchMinorArchives()
          } else {
            this.showNotif(
              'negative',
              "Errore durante l'archiviazione del minore"
            )
          }
        })
        .catch(() => {
          this.showNotif(
            'negative',
            "Errore durante l'archiviazione del minore"
          )
        })
    },
    getMinors(url = '') {
      let path =
        '/minors/minor?page=' +
        (this.pagination.page - 1) +
        '&limit=' +
        this.pagination.rowsPerPage
      if (url.trim() !== '') {
        path += url
      }
      path += '&status=enabled'
      api
        .get(path)
        .then(response => {
          if (!Array.isArray(response.data)) {
            this.rows = response.data.paginatedResults.map(v => ({
              ...v,
              isPresent: false,
              id: v._id.$oid
            }))
            this.pagination = response.data.meta
          } else {
            this.rows = []
          }

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
        const res = this.minor
        if (res.fiscal_code.trim() === '') {
          delete res.fiscal_code
        }
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
              this.getMinors()
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
    edit(row) {
      this.dialog = true
      this.editedId = row._id.$oid
      this.minor = {
        name: row.name,
        surname: row.surname,
        fiscal_code: row.fiscal_code
      }
      this.isEdit = true
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
              this.getMinors()
            } else if (resp.data?.msg) {
              this.showNotif('warning', resp.data.msg)
            } else {
              this.showNotif(
                'negative',
                'Errore durante la modifica del minore'
              )
            }
          })
          .catch(() => {
            this.showNotif('negative', 'Errore durante la modifica del minore')
            this.dialog = false
            this.editedId = null
          })
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
    deleteMinor(row) {
      api
        .put('/minors/minor/disable/' + row._id.$oid)
        .then(resp => {
          if (resp.data.success) {
            this.showNotif('positive', 'Minore eliminato con successo')
            api.post('/auth/log', {
              name: 'Eliminazione minore : ' + row.name + ' ' + row.surname,
              description: 'Minore eliminato correttamente',
              color: 'green'
            })
            this.today = moment(String(this.today)).format('YYYY/MM/DD')
            this.getMinors()
          } else if (resp.data?.msg) {
            this.showNotif('warning', resp.data.msg)
          } else {
            this.showNotif(
              'negative',
              "Errore durante l'eliminazione del minore"
            )
          }
        })
        .catch(() => {
          this.showNotif('negative', "Errore durante l'eliminazione del minore")
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
    viewArchive(archiveId) {
      api
        .get('/exports/archive/minor/' + archiveId)
        .then(response => {
          const blob = this.dataURItoBlob(response.data)
          const url = URL.createObjectURL(blob)
          window.open(url, '_blank')
        })
        .catch(() => {
          this.showNotif(
            'negative',
            "Impossibile visualizzare l'archivio al momento"
          )
        })
    },
    view(row) {
      api
        .get('/exports/export/minor/' + row._id.$oid)
        .then(response => {
          const blob = this.dataURItoBlob(response.data.file)
          const url = URL.createObjectURL(blob)
          window.open(url, '_blank')
        })
        .catch(er => {
          this.showNotif('negative', "Impossibile eseguire l'export al momento")
        })
    },
    viewAIReport(row) {
      api
        .get(`/exports/export/minor/ai/${row._id.$oid}`)
        .then(response => {
          const blob = this.dataURItoBlob(response.data.file)
          const url = URL.createObjectURL(blob)
          window.open(url, '_blank')

          this.$q.loading.hide()
          this.showNotif('positive', 'Report AI generato con successo')
        })
        .catch(error => {
          this.$q.loading.hide()
          console.error('Errore durante la generazione del report AI:', error)
          this.showNotif(
            'negative',
            'Impossibile generare il report AI al momento'
          )
        })
    },
    editFile(row) {
      this.$router.push({
        name: 'minor_info_sheet',
        params: {
          id: row._id.$oid,
          isFirstPriceEdit:
            !row.info_sheet || !((row.modified ?? 'false') === 'true')
        }
      })
    },
    reset() {
      this.dialog = false
      this.minor = { name: '', surname: '', fiscal_code: '' }
    },
    isValidFiscalCode(val) {
      const fiscalPattern =
        /^([A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST]{1}[0-9LMNPQRSTUV]{2}[A-Z]{1}[0-9LMNPQRSTUV]{3}[A-Z]{1})$|([0-9]{11})$/
      if (!val || val.trim().length === 0) {
        return true
      } else {
        return (
          fiscalPattern.test(val.toUpperCase()) || 'Codice fiscale non valido'
        )
      }
    },
    watchFilterDate(value, reason, detail) {
      this.filters.entry_date = moment(value).format('DD/MM/YYYY')
    },
    addFilters(url) {
      Object.keys(this.filters).forEach(el => {
        if (typeof this.filters[el] === 'string') {
          if (this.filters[el].trim() !== '') {
            if (el === 'fiscal_code') {
              this.filters[el] = this.filters[el].toUpperCase()
            }
            url += '&' + el + '=' + this.filters[el]
          }
        } else if (typeof this.filters[el] === 'number') {
          if (this.filters[el] > 0) {
            url += '&' + el + '=' + this.filters[el]
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
        this.getMinors(url)
      } else {
        this.showNotif('info', 'Non è stato inserito alcun filtro')
      }
    },
    resetFilters() {
      this.expanded = false

      this.filters = {
        name: '',
        surname: '',
        fiscal_code: '',
        entry_date: null
      }
      this.getMinors()
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

#expansioned_item {
  width: 100%;
  background: white;
  box-shadow: rgb(0 0 0 / 20%) 0px 1px 5px, rgb(0 0 0 / 14%) 0px 2px 2px,
    rgb(0 0 0 / 12%) 0px 3px 1px -2px;
  border-radius: 5px;
  margin-bottom: 10px;
}
q-btn-dropdown [aria-expanded='false'] {
  border-radius: 15px;
}

q-btn-dropdown[aria-expanded='true'] {
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  border-bottom-left-radius: 0px;
  border-bottom-right-radius: 0px;
}
</style>
