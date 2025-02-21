<template>
  <q-page class="q-mx-xl">
    <div class="row"><Heading :title="'Tariffe Adulti'" /></div>
    <div class="row q-ma-md">
      <q-table
        v-model:pagination="pagination"
        :rows="rows"
        :columns="columns"
        row-key="id"
        :loading="data_loading"
        :rows-per-page-options="[5, 8, 10, 15, 25, 50]">
        <template #body-cell-start_date="props">
          <q-td style="text-align: center"
            >{{
              (props.row.price?.history[0]?.timestamp ?? '')
                .split('-')
                .reverse()
                .join('/')
            }}
          </q-td>
        </template>
        <template #body-cell-price="props">
          <q-td style="text-align: center"
            >{{ props.row.price?.value ?? '0' }} €
          </q-td>
        </template>
        <template #body-cell-actions="props">
          <q-td
            style="display: flex; justify-content: center; align-items: center">
            <q-btn
              round
              icon="visibility"
              :disable="(props.row.price?.history?.length ?? 0) === 0"
              color="blue"
              size="sm"
              @click="viewHistory(props.row)" />
            <q-btn
              round
              icon="edit"
              color="green"
              size="sm"
              class="q-ml-lg"
              @click="showAddTariff(props.row)" />
          </q-td>
        </template>
      </q-table>
    </div>
    <q-dialog v-model="popupViewHistory">
      <q-card class="q-pb-md" style="width: 400px">
        <q-card-section>
          <div class="text-h6">
            {{ popupViewHistoryRow.name + ' ' + popupViewHistoryRow.surname }}
          </div>
        </q-card-section>
        <q-card-section>
          <q-item class="q-pl-none">
            <q-item-label>Storico tariffe</q-item-label>
          </q-item>
          <div style="max-height: 300px; overflow-y: scroll">
            <q-list bordered separator>
              <q-item
                v-for="item in popupViewHistoryRow.price?.history ?? []"
                :key="item.timestamp">
                <q-item-section>{{
                  (item.timestamp ?? '').split('-').reverse().join('/')
                }}</q-item-section>
                <q-item-section
                  side
                  avatar
                  style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: row;
                  ">
                  <span> {{ item.value ?? '' }} € </span>
                  <q-btn
                    round
                    dense
                    flat
                    color="red"
                    icon="delete"
                    class="q-ml-sm"
                    @click="
                      askConfirm(
                        'Sei sicuro di voler eliminare la tariffa?',
                        deleteTariff,
                        popupViewHistoryRow.id,
                        item.timestamp
                      )
                    " />
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
    <q-dialog v-model="popupAddTariffs">
      <q-card class="q-pb-md" style="width: 400px">
        <q-card-section>
          <div class="text-h6">
            {{
              popupAddTariffsRow.name ??
              '' + ' ' + popupAddTariffsRow.surname ??
              ''
            }}
          </div>
        </q-card-section>
        <q-card-section
          style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
          ">
          <q-input
            v-model="newTariffPrice"
            outlined
            label="Prezzo nuova tariffa"
            type="number"
            color="primary"
            class="q-mb-md"
            style="width: 100%" />
          <q-date
            v-model="newTariffDate"
            mask="YYYY/MM/DD"
            color="primary"
            title="Data inizio tariffa"
            :locale="locale"
            class="q-mb-md"
            today-btn
            outlined />
        </q-card-section>
        <q-card-section align="right" class="text-primary">
          <q-btn color="secondary" @click="addTariff(popupAddTariffsRow.id)">
            Salva
          </q-btn>
          <q-btn
            label="Cancella"
            type="reset"
            color="primary"
            flat
            class="q-ml-sm"
            @click="popupAddTariffs = false" />
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import Heading from 'components/Heading.vue'
import { useQuasar } from 'quasar'
import { api } from 'src/boot/axios'
export default {
  name: 'AdultsTariffs',
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
  data: function () {
    return {
      locale: {
        days: 'Domenica_Lunedì_Martedì_Mercoledì_Giovedì_Venerdì_Sabato'.split(
          '_'
        ),
        daysShort: 'Dom_Lun_Mar_Mer_Gio_Ven_Sab'.split('_'),
        months:
          'Gennaio_Febbraio_Marzo_Aprile_Maggio_Giugno_Luglio_Agosto_Settembre_Ottobre_Novembre_Dicembre'.split(
            '_'
          ),
        monthsShort: 'Gen_Feb_Mar_Apr_Mag_Giu_Lug_Ago_Set_Ott_Nov_Dic'.split(
          '_'
        ),
        firstDayOfWeek: 1,
        today: 'Oggi',
        clear: 'Cancella'
      },
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
          name: 'start_date',
          align: 'center',
          label: 'Data inizio tariffa',
          field: 'start_date'
        },

        {
          name: 'price',
          align: 'center',
          label: 'Prezzo'
        },
        {
          name: 'actions',
          align: 'center',
          label: 'Azioni'
        }
      ],
      pagination: {
        page: 0,
        rowsPerPage: 8
      },
      rows: [],
      popupViewHistory: false,
      popupAddTariffs: false,
      popupViewHistoryRow: {},
      popupAddTariffsRow: {},
      newTariffPrice: 0,
      newTariffDate: new Date().toISOString().slice(0, 10).replace(/-/g, '/'),
      data_loading: false,
      tariffs: [],
      adults: []
    }
  },
  watch: {
    popupAddTariffs(val) {
      if (!val) {
        this.newTariffPrice = 0
      }
    },
    adults() {
      this.rows = this.formatAdults(this.adults)
    },
    tariffs() {
      this.rows = this.formatAdults(this.adults)
    }
  },
  mounted() {
    this.populateTable()
  },

  methods: {
    viewHistory(row) {
      this.popupViewHistoryRow = row
      this.popupViewHistory = true
    },
    showAddTariff(row) {
      this.popupAddTariffsRow = row
      this.popupAddTariffs = true
    },

    formatAdults(adults) {
      try {
        return adults.map(m => {
          return {
            ...m,
            price: this.tariffs.find(t => t.adult_id === m._id.$oid),
            id: m._id.$oid
          }
        })
      } catch (error) {
        this.showNotif('negative', 'Errore nel caricamento dei dati')
        return []
      }
    },

    async populateTable() {
      this.getAdults()
      this.getTariffs()
    },

    async getTariffs() {
      this.data_loading = true
      try {
        const response = await api.get('adults/adult/price')
        this.tariffs = response.data
        this.data_loading = false
      } catch (error) {
        this.showNotif('negative', 'Errore nel caricamento delle tariffe')
        this.data_loading = false
      }
    },
    async getAdults() {
      const path = '/adults/adult/all'
      try {
        const response = await api.get(path)
        this.adults = response.data
        this.data_loading = false
      } catch (error) {
        this.showNotif('negative', 'Errore nel caricamento degli adulti')
        this.data_loading = false
      }
    },

    async addTariff(adultId) {
      const path = '/adults/adult/' + adultId + '/price'
      try {
        await api.post(path, {
          value: parseFloat(this.newTariffPrice),
          timestamp: this.newTariffDate.replace(/\//g, '-')
        })
        this.showNotif('positive', 'Tariffa aggiunta con successo')
        this.popupAddTariffs = false
        this.populateTable()
      } catch (error) {
        this.showNotif('negative', "Errore nell'aggiunta della tariffa")
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
    async deleteTariff(adultId, timestamp) {
      this.popupViewHistory = false

      const path = '/adults/adult/' + adultId + '/price/' + timestamp
      try {
        await api.delete(path)
        this.showNotif('positive', 'Tariffa eliminata con successo')
        this.populateTable()
      } catch (error) {
        this.showNotif('negative', "Errore nell'eliminazione della tariffa")
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

::-webkit-scrollbar {
  width: 12px;
}

/* Track */
::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  -webkit-border-radius: 0px 10px 10px 0px;
  border-radius: 0px 10px 10px 0px;
}

/* Handle */
::-webkit-scrollbar-thumb {
  -webkit-border-radius: 0px 10px 10px 0px;
  border-radius: 0px 10px 10px 0px;
  background: #d4d4d4;
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
}
::-webkit-scrollbar-thumb:window-inactive {
  background: #d4d4d4;
}
</style>
