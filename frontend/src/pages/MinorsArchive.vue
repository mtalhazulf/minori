<template>
  <q-page class="q-mx-xl">
    <div class="row"><Heading :title="'Archivio Minori'" /></div>
    <div class="row">
      <q-table
        v-model:pagination="pagination"
        :rows="rows"
        :columns="columns"
        row-key="id"
        :loading="data_loading"
        :rows-per-page-options="[5, 8, 10, 15, 25, 50]"
        @request="onRequest">
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
        <template #body-cell-deactivation_date="props">
          <q-td :props="props">{{
            props.row.deactivation_date
              ? convertDate(props.row.deactivation_date)
              : ''
          }}</q-td>
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
                    ? 'Impossibile caricare i minori al momento..'
                    : 'Nessun minore presente ...'
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
  name: 'MinorsArchive',
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
          name: 'deactivation_date',
          align: 'center',
          label: 'Data di disattivazione',
          field: 'deactivation_date',
          sortable: true
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
      pagination: {
        page: 0,
        rowsPerPage: 8
      },
      isEdit: false,
      editedId: null,
      close: false,
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
    getMinors() {
      api
        .get(
          `/minors/minor?page=${this.pagination.page - 1}&limit=${
            this.pagination.rowsPerPage
          }&status=disabled`
        )
        .then(response => {
          this.rows = response.data.paginatedResults
          this.pagination = reqsponse.data.meta
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
    convertDate(date) {
      return moment(String(date)).format('DD/MM/YYYY')
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
