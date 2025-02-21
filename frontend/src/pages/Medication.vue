f
<template>
  <q-page class="q-mx-xl">
    <div class="row"><Heading :title="'Farmaci'" /></div>
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
                style="background: white; width: 170px" /><q-input
                v-model.number="filters.amount"
                type="number"
                class="q-ma-md"
                outlined
                style="background: white; width: 170px"
                label="Quantità: "
                :rules="[
                  val =>
                    expanded === false
                      ? true
                      : val >= 1 || 'Inserire una quantità valida'
                ]" />

              <q-select
                v-model="filters.operator"
                outlined
                class="q-ma-md"
                label="Operatore"
                :options="operators.length === 0 ? [] : operators"
                :option-label="opt => opt.name + ' ' + opt.surname"
                emit-value
                style="width: 17%"
                ><template #no-option>
                  <q-item>
                    <q-item-section class="text-italic text-grey">
                      Nessun operatore disponibile
                    </q-item-section>
                  </q-item>
                </template></q-select
              >
              <q-input
                v-model="filters.expiration_date"
                outlined
                class="q-ma-md"
                label="Scadenza dopo: "
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
              <q-select
                v-model="filters.disposed_of"
                outlined
                :options="medicationOptionsDisposed"
                label="Smaltimento"
                style="width: 17%"
                class="q-ma-md"
                emit-value
                ><template #selected-item="scope">
                  {{
                    medicationOptionsDisposed.find(x => x.value === scope.opt)
                      .label
                  }}
                </template></q-select
              >
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
            style="width: 176px"
            @click="
              () => {
                isEdit = false
                dialog = true
              }
            ">
            Aggiungi Farmaco</q-btn
          >
          <q-dialog v-model="dialog" persistent>
            <q-card>
              <q-card-section>
                <div class="text-h6">Aggiungi Farmaco</div>
              </q-card-section>
              <q-form class="q-gutter-md">
                <q-card-section>
                  <q-input
                    v-model="medicinal.name"
                    outlined
                    class="q-my-sm"
                    label="Nome"
                    style="text-transform: uppercase" />
                  <q-input
                    v-model="medicinal.lotto"
                    outlined
                    class="q-my-sm"
                    label="Lotto" />
                  <q-input
                    v-model.number="medicinal.amount"
                    type="number"
                    class="q-my-sm"
                    outlined
                    style="max-width: 200px"
                    label="Inserisci quantità: "
                    :rules="[
                      val => val >= 1 || 'Inserire una quantità valida'
                    ]" />
                  <q-input
                    v-model="medicinal.expiration_date"
                    outlined
                    class="q-my-sm"
                    label="Inserisci data di scadenza: "
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
                  <q-checkbox
                    v-model="medicinal.disposed_of"
                    :label="
                      medicinal.disposed_of ? 'Smaltito' : 'Non smaltito'
                    " />
                </q-card-section>

                <q-card-section align="right" class="text-primary">
                  <q-btn
                    color="secondary"
                    :loading="loading"
                    :disable="validateForm()"
                    style="width: 150px"
                    @click="isEdit ? editMedicinal() : save()">
                    Salva
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
        <template #body-cell-expiration_date="props">
          <q-td :props="props">
            <div>
              {{ convertDate(props.row.expiration_date) }}
            </div>
          </q-td>
        </template>
        <template #body-cell-disposed_of="props">
          <q-td :props="props">
            <div>
              <q-icon
                :name="props.row.disposed_of ? 'check_circle' : 'highlight_off'"
                size="1.5em"
                :color="props.row.disposed_of ? 'green' : 'red'" />
            </div>
          </q-td>
        </template>
        <template #body-cell-creation_user="props">
          <q-td :props="props">
            <div>
              {{
                typeof props.row.creation_user === 'string'
                  ? props.row.creation_user
                  : props.row.creation_user?.name
                  ? props.row.creation_user.name +
                    ' ' +
                    props.row.creation_user.surname
                  : props.row.creation_user.companyName
              }}
            </div>
          </q-td>
        </template>
        <template #body-cell-actions="props">
          <q-td>
            <q-btn
              round
              icon="edit"
              color="green"
              size="sm"
              style="margin-left: 30%"
              @click="edit(props.row)" />
            <q-btn
              round
              icon="delete"
              color="red"
              size="sm"
              class="q-ml-lg"
              @click="
                askConfirm(
                  'Sei sicuro di voler eliminare il farmaco?',
                  deleteMedication,
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
                    ? 'Impossibile caricare i farmaci al momento..'
                    : 'Nessun farmaco presente ...'
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
import { date } from 'quasar'

export default {
  name: 'Medication',
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
          field: 'name',
          sortable: true
        },
        {
          name: 'lotto',
          align: 'center',
          label: 'Lotto',
          field: 'lotto',
          sortable: true
        },
        {
          name: 'amount',
          align: 'center',
          label: 'Quantità',
          field: 'amount',
          sortable: true
        },
        {
          name: 'creation_user',
          align: 'center',
          label: 'Creato da ',
          field: 'creation_user',
          sortable: true
        },
        {
          name: 'expiration_date',
          align: 'center',
          label: 'Data scadenza',
          field: 'expiration_date',
          sortable: true
        },
        {
          name: 'disposed_of',
          align: 'center',
          label: 'Smaltito',
          field: 'disposed_of',
          sortable: true
        },
        {
          name: 'actions',
          align: 'center',
          label: 'Azioni',
          sortable: true
        }
      ],
      loading: false,
      data_loading: true,
      errDataMsg: false,
      dialog: false,
      medicinal: {
        name: '',
        expiration_date: '',
        lotto: '',
        amount: '',
        disposed_of: false
      },
      pagination: {
        page: 0,
        rowsPerPage: 8
      },
      editedId: null,
      isEdit: false,
      filters: {
        name: '',
        amount: '',
        operator: null,
        expiration_date: null,
        disposed_of: null
      },
      medicationOptionsDisposed: [
        { label: 'Smaltiti', value: true },
        { label: 'Non smaltiti', value: false }
      ],
      expanded: false,
      operators: []
    }
  },
  watch: {
    'medicinal.expiration_date'(newDate, oldDate) {
      return moment(newDate).format('DD/MM/YYYY')
    }
  },
  mounted() {
    this.getMedications()
    this.getOperators()
  },
  methods: {
    onRequest(props) {
      const { page, rowsPerPage } = props.pagination
      this.pagination.page = page
      this.pagination.rowsPerPage = rowsPerPage
      this.getMedications()
    },

    getMedications(url = '') {
      let path =
        '/tasks/medication?page=' +
        (this.pagination.page - 1) +
        '&limit=' +
        this.pagination.rowsPerPage
      if (url.trim() !== '') {
        path += url
      }
      api
        .get(path)
        .then(response => {
          if (!Array.isArray(response.data)) {
            this.rows = response.data.paginatedResults
            this.pagination = response.data.meta
          } else {
            this.rows = []
          }
          setTimeout(() => {
            this.errDataMsg = false
            this.data_loading = false
          }, 500)
          this.$store.commit('updateMedications', this.rows)
        })
        .catch(() => {
          this.errDataMsg = true
          this.data_loading = false
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
    addMedication() {
      this.medicinal.name = this.medicinal.name.toUpperCase()
      api
        .post('/tasks/medication', this.medicinal)
        .then(resp => {
          setTimeout(() => {
            this.loading = false
            this.showNotif('positive', 'Farmaco caricato correttamente.')
            this.dialog = false
            this.reset()
          }, 500)
          const operatorName = JSON.parse(sessionStorage.getItem('user')).name
          api.post('/auth/log', {
            name: 'Aggiunta farmaco : ' + this.medicinal.name,
            description: 'Farmaco aggiunto correttamente',
            color: 'green'
          })
          this.getMedications()
        })
        .catch(error => {
          setTimeout(() => {
            this.loading = false
            this.showNotif(
              'negative',
              'Il farmaco non è stato inserito correttamente.'
            )
            this.dialog = false
            this.reset()
          }, 500)
        })
    },
    save() {
      this.loading = true
      this.addMedication()
    },
    edit(row) {
      this.dialog = true
      this.editedId = row._id.$oid
      this.medicinal = {
        name: row.name,
        expiration_date: this.convertDate(row.expiration_date),
        lotto: row.lotto,
        amount: row.amount,
        disposed_of: row?.disposed_of ? row.disposed_of : false
      }
      this.isEdit = true
    },
    editMedicinal() {
      this.loading = true
      this.medicinal.name = this.medicinal.name.toUpperCase()
      api
        .put('/tasks/medication/' + this.editedId, this.medicinal)
        .then(resp => {
          setTimeout(() => {
            this.loading = false
            this.showNotif('positive', 'Farmaco modificato correttamente.')
            this.dialog = false
            this.reset()
          }, 500)
          this.getMedications()
        })
        .catch(error => {
          setTimeout(() => {
            this.loading = false
            this.showNotif(
              'negative',
              'Il farmaco non è stato modificato correttamente.'
            )
            this.dialog = false
            this.reset()
          }, 500)
        })
    },
    convertDate(date) {
      return moment(String(date)).format('DD/MM/YYYY')
    },
    reset() {
      this.dialog = false
      this.medicinal = {
        name: '',
        expiration_date: '',
        lotto: '',
        amount: '',
        disposed_of: false
      }
    },
    watchDate(value, reason, detail) {
      this.medicinal.expiration_date = moment(value).format('DD/MM/YYYY')
    },
    watchFilterDate(value, reason, detail) {
      this.filters.expiration_date = moment(value).format('DD/MM/YYYY')
    },
    validateForm() {
      if (
        this.medicinal.name === '' ||
        this.medicinal.name.trim() === '' ||
        this.medicinal.expiration_date === '' ||
        this.medicinal.expiration_date.trim() === '' ||
        this.medicinal.amount < 1 ||
        this.medicinal.amount === undefined
      ) {
        return true
      } else {
        return false
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
    deleteMedication(row) {
      api
        .delete('/tasks/medication/' + row._id.$oid)
        .then(resp => {
          if (resp.data.success) {
            this.showNotif('positive', 'Farmaco eliminato correttamente.')
            api.post('/auth/log', {
              name: 'Eliminazione farmaco : ' + row.name,
              description: 'Farmaco eliminato correttamente',
              color: 'green'
            })
            this.getMedications()
          } else {
            this.showNotif(
              'negative',
              "Errore durante l'eliminazione del farmaco."
            )
          }
        })
        .catch(error => {
          this.showNotif(
            'negative',
            "Errore durante l'eliminazione del farmaco."
          )
        })
    },
    addFilters(url) {
      Object.keys(this.filters).forEach(el => {
        if (typeof this.filters[el] === 'string') {
          if (this.filters[el].trim() !== '') {
            url += '&' + el + '=' + this.filters[el].toUpperCase()
          }
        } else if (typeof this.filters[el] === 'number') {
          if (this.filters[el] > 0) {
            url += '&' + el + '=' + this.filters[el]
          }
        } else if (typeof this.filters[el] === 'object') {
          if (this.filters[el] !== null) {
            url += '&' + el + '=' + this.filters[el]._id.$oid
          }
        } else if (typeof this.filters[el] === 'boolean') {
          if (this.filters[el] !== null) {
            url += '&' + el + '=' + this.filters[el]
          }
        }
      })
      return url
    },
    applyFilters() {
      let url = ''
      url = this.addFilters(url)
      if (url !== '') {
        this.getMedications(url, 0)
      } else {
        this.showNotif('info', 'Non è stato inserito alcun filtro')
      }
    },
    resetFilters() {
      this.expanded = false

      this.filters = {
        name: '',
        amount: null,
        operator: null,
        expiration_date: null
      }
      this.getMedications()
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

#expansioned_item {
  width: 100%;
  background: white;
  box-shadow: rgb(0 0 0 / 20%) 0px 1px 5px, rgb(0 0 0 / 14%) 0px 2px 2px,
    rgb(0 0 0 / 12%) 0px 3px 1px -2px;
  border-radius: 5px;
  margin-bottom: 10px;
}
</style>
