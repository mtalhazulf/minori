<template>
  <q-page class="q-mx-xl">
    <div class="row">
      <Heading :title="'Archivio Operatori'" />
    </div>
    <div class="row">
      <q-table
        v-model:pagination="pagination"
        :rows="rows"
        :columns="columns"
        row-key="id"
        :loading="data_loading"
        :rows-per-page-options="[5, 8, 10, 15, 25, 50]">
        <template #body-cell-role="props">
          <q-td :props="props">
            {{
              props.row?.role
                ? props.row.role.name + ' - ' + props.row.role.label
                : ''
            }}
          </q-td>
        </template>
        <template #body-cell-deactivation_date="props">
          <q-td :props="props">{{
            convertDate(props.row.deactivation_date)
          }}</q-td>
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
  name: 'OperatorArchive',
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
          name: 'email',
          align: 'center',
          label: 'Email',
          field: 'email',
          sortable: true
        },
        {
          name: 'deactivation_date',
          align: 'center',
          label: 'Data di disattivazione',
          field: 'deactivation_date',
          sortable: true
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
      close: false
    }
  },
  mounted() {
    this.getOperators()
  },
  methods: {
    getOperators() {
      api
        .get('/auth/user/operators?status=disabled')
        .then(response => {
          this.rows = response.data
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
