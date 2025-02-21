<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar class="q-pb-sm q-pt-sm">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          class="toolbar_size"
          @click="toggleLeftDrawer" />

        <q-toolbar-title class="toolbar_size" @click="$router.push('/')">
          <span>Home</span>
        </q-toolbar-title>

        <div class="toolbar_size">
          {{
            operator.name
              ? operator.name + ' ' + operator.surname
              : operator.companyName
          }}
          <q-btn flat round dense icon="person" class="toolbar_size">
            <q-menu>
              <q-list dense style="min-width: 100px">
                <q-item
                  v-close-popup
                  clickable
                  @click="$router.push('/change_password')">
                  <q-item-section class="q-my-sm"
                    >Cambio password</q-item-section
                  >
                </q-item>
                <q-item v-close-popup clickable @click="beforeLogout()">
                  <q-item-section class="q-my-sm">Logout</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <div style="display: flex; align-items: center">
      <q-dialog v-model="dialog">
        <q-card
          ><q-banner
            v-if="!childPresence && new Date().getHours() < 14"
            inline-actions
            class="text-white bg-orange">
            Attenzione! Compilare il
            <q-btn
              flat
              no-caps
              @click="
                () => {
                  $router.push('/minor_register')
                  dialog = false
                }
              ">
              Registro dei i
            </q-btn>
          </q-banner>
          <q-card-section>
            <div class="text-h6">Controllo Logout</div>
          </q-card-section>
          <q-separator inset />
          <q-card-section class="q-pt-none">
            Prima di andare via assicurarsi di aver effettuato tutte le consegne
            e mansioni prese in carico.
          </q-card-section>
          <q-card-section class="q-pt-none">
            Controlla il
            <q-btn
              outline
              @click="
                () => {
                  $router.push('/logbook')
                  dialog = false
                }
              ">
              Diario di bordo
            </q-btn>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn
              v-close-popup
              flat
              label="Chiudi"
              color="primary"
              @click="dialog = false" />
            <q-btn label="Logout" color="primary" @click="logout()" />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header> Links </q-item-label>
        <div v-for="link in essentialLinks" :key="link.title">
          <div v-if="link?.children">
            <q-expansion-item
              v-if="
                link.auth.includes(operator.usertype) &&
                checkAuth(link.children)
              "
              expand-separator
              :icon="link.icon"
              :label="link.title"
              @click="
                link.to
                  ? $router.push(link.to)
                  : link.redirect_to
                  ? redirect(link.redirect_to)
                  : ''
              ">
              <div v-if="link?.children">
                <EssentialLink
                  v-for="l in link.children"
                  :key="l.title"
                  v-bind="l"
                  class="q-ml-md"
                  @click="leftDrawerOpen = !leftDrawerOpen" />
              </div>
            </q-expansion-item>
          </div>
          <div v-else>
            <q-item
              v-if="link.auth.includes(operator.usertype)"
              clickable
              tag="a"
              target="_blank"
              @click="
                link.to
                  ? $router.push(link.to)
                  : link.redirect_to
                  ? redirect(link.redirect_to)
                  : ''
              ">
              <q-item-section v-if="link.icon" avatar>
                <q-icon :name="link.icon" />
              </q-item-section>

              <q-item-section>
                <q-item-label>{{ link.title }}</q-item-label>
                <q-item-label caption>
                  {{ link.caption }}
                </q-item-label>
              </q-item-section>
            </q-item>
          </div>
        </div>
      </q-list>
    </q-drawer>

    <q-page-container style="background: #f2f2f27a">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import EssentialLink from 'components/EssentialLink.vue'

const linksList = [
  {
    title: 'Dashboard',
    caption: '',
    icon: 'dashboard',
    to: '/',
    auth: ['superadmin', 'admin', 'user']
  },
  {
    title: 'Attività',
    caption: '',
    icon: 'auto_stories',
    auth: ['superadmin', 'admin', 'user'],
    children: [
      {
        title: 'Mansionario',
        caption: '',
        icon: 'auto_stories',
        to: '/notebook',
        auth: ['superadmin', 'admin', 'user']
      },
      {
        title: 'Diario di bordo',
        caption: '',
        icon: 'library_books',
        to: '/logbook',
        auth: ['superadmin', 'admin', 'user']
      },
      {
        title: 'Quaderno delle Consegne',
        caption: '',
        icon: 'format_list_bulleted',
        to: '/tasks',
        auth: ['superadmin', 'admin', 'user']
      }
    ]
  },
  {
    title: 'Stanze',
    caption: '',
    icon: 'meeting_room',
    to: '/rooms',
    auth: ['superadmin', 'admin']
  },
  {
    title: 'Scadenzario',
    caption: '',
    icon: 'event',
    to: '/scheduler',
    auth: ['superadmin', 'admin']
  },
  {
    title: 'Turni',
    caption: '',
    icon: 'event',
    to: '/shifts',
    auth: ['superadmin', 'admin']
  },
  {
    title: 'Turni',
    caption: '',
    icon: 'event',
    to: '/operator-shifts',
    auth: ['user']
  },
  {
    title: 'Farmaci',
    caption: '',
    icon: 'medication',
    to: '/medication',
    auth: ['superadmin', 'admin', 'user']
  },
  {
    title: 'Registro Telefonate',
    caption: '',
    icon: 'phone_in_talk',
    to: '/phone_call_log',
    auth: ['superadmin', 'admin', 'user']
  },
  {
    title: 'Gestione Operatori',
    caption: '',
    icon: 'list',
    auth: ['superadmin', 'admin'],
    children: [
      {
        title: 'Operatori',
        caption: '',
        icon: 'list',
        to: '/operators',
        auth: ['superadmin', 'admin']
      },
      {
        title: 'Archivio operatori',
        caption: '',
        icon: 'inventory_2',
        to: '/operator_archive',
        auth: ['superadmin', 'admin']
      },
      {
        title: 'Registro presenze operatori',
        caption: '',
        icon: 'list_alt',
        to: '/operator_register',
        auth: ['superadmin', 'admin']
      }
    ]
  },
  {
    title: 'Gestione Ospiti',
    caption: '',
    icon: 'description',
    auth: ['superadmin', 'admin', 'user'],
    children: [
      {
        title: 'Registro presenze minori',
        caption: '',
        icon: 'list_alt',
        to: '/minor_register',
        auth: ['superadmin', 'admin', 'user']
      },
      {
        title: 'Fascicolo minori',
        caption: '',
        icon: 'escalator_warning',
        to: '/minors',
        auth: ['superadmin', 'admin']
      },

      {
        title: 'Archivio minori',
        caption: '',
        icon: 'inventory_2',
        to: '/minors_archive',
        auth: ['superadmin', 'admin']
      },
      {
        title: 'Gestione tariffe minori',
        caption: '',
        icon: 'payments',
        to: '/minors_tariffs',
        auth: ['superadmin', 'admin']
      },
      {
        title: 'Registro presenze adulti',
        caption: '',
        icon: 'list_alt',
        to: '/adult_register',
        auth: ['superadmin', 'admin', 'user']
      },
      {
        title: 'Fascicolo adulti',
        caption: '',
        icon: 'person',
        to: '/adults',
        auth: ['superadmin', 'admin']
      },
      {
        title: 'Archivio adulti',
        caption: '',
        icon: 'inventory_2',
        to: '/adults_archive',
        auth: ['superadmin', 'admin']
      },
      {
        title: 'Gestione tariffe adulti',
        caption: '',
        icon: 'payments',
        to: '/adults_tariffs',
        auth: ['superadmin', 'admin']
      }
    ]
  },
  {
    title: 'Impostazioni',
    caption: '',
    icon: 'settings',
    to: '/settings',
    auth: ['superadmin', 'admin']
  },
  {
    title: 'Reportistica',
    caption: '',
    icon: 'file_download',
    to: '/reports',
    auth: ['superadmin', 'admin']
  },
  {
    title: 'Catalogo Incentivi',
    caption: '',
    icon: 'euro_symbol',
    to: '/catalogo',
    auth: ['superadmin', 'admin', 'user']
  },
  {
    title: 'Saved Incentivi',
    caption: '',
    icon: 'manage_accounts',
    to: '/incentivi',
    auth: ['superadmin', 'admin', 'user']
  }
]

import { defineComponent, ref } from 'vue'
import { api } from 'src/boot/axios'
import moment from 'moment'

export default defineComponent({
  name: 'MainLayout',

  components: {
    EssentialLink
  },
  setup() {
    const leftDrawerOpen = ref(false)

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  },
  data() {
    return {
      operator: '',
      dialog: false,
      childPresence: false,
      menuList: linksList
    }
  },
  mounted() {
    this.operator = JSON.parse(sessionStorage.getItem('user'))

    // Check if 'Rendicontazione' already exists in the linksList
    const rendicontazioneExists = linksList.some(
      link => link.title === 'Rendicontazione'
    )

    if (!rendicontazioneExists) {
      linksList.push({
        title: 'Rendicontazione',
        caption: '',
        icon: 'manage_accounts',
        redirect_to: process.env.APP_REPORT_URL,
        auth: ['superadmin']
      })
    }
  },
  methods: {
    getMinorAttendance() {
      api
        .get('/minors/attendance', {
          params: {
            current_date: moment(String(new Date())).format('YYYY/MM/DD')
          }
        })
        .then(response => {
          this.childPresence = response.data.length > 0 ? true : false
        })
    },
    checkIfDisplay() {
      const now = new Date().getHours()
      if (now >= 0 && now < 14) {
        return true
      } else {
        return false
      }
    },
    isAlreadyInserted() {
      return this.essentialLinks.find(el => el.to === '/minor_register')
    },
    beforeLogout() {
      if (
        this.operator.usertype === 'admin' ||
        this.operator.usertype === 'superadmin'
      ) {
        this.logout()
      } else {
        this.getMinorAttendance()
        this.dialog = true
      }
    },
    redirect(url) {
      window.location.href =
        url + '?jwt=' + sessionStorage.getItem('access-token')
    },
    checkAuth(link) {
      return link.filter(x => x.auth.includes(this.operator.usertype)).length >
        0
        ? true
        : false
    },
    logout() {
      api.post('/auth/logout', { user: this.operator.uid }).then(response => {
        this.$store.commit('updateLoginStatus', false)
        sessionStorage.removeItem('user')
        sessionStorage.removeItem('access-token')
        this.$router.go('/')
      })
    }
  }
})
</script>

<style scoped>
.q-toolbar {
  background: #019a29;
}

@media (min-width: 600px) {
  .q-dialog__inner--minimized > div {
    min-width: 306px;
  }
}

span {
  cursor: pointer;
}
</style>
