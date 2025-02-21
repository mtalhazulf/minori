<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex bg-image flex-center">
        <q-card :style="$q.screen.lt.sm ? { width: '80%' } : { width: '30%' }">
          <q-card-section>
            <q-avatar
              size="103px"
              class="absolute-center shadow-10"
              color="white"
              text-color="grey"
              font-size="130px"
              icon="person" />
          </q-card-section>
          <q-card-section>
            <div class="text-center q-pt-lg">
              <div class="col text-h6 ellipsis">Login</div>
            </div>
          </q-card-section>
          <q-form class="q-gutter-md">
            <q-card-section>
              <div>
                <q-input
                  v-model="operator.username"
                  class="q-mb-md"
                  filled
                  label="Username" />
                <q-input
                  v-model="operator.password"
                  filled
                  class="q-my-md"
                  :type="isPwd ? 'password' : 'text'"
                  placeholder="Enter Password">
                  <template #append>
                    <q-icon
                      :name="isPwd ? 'visibility_off' : 'visibility'"
                      class="cursor-pointer"
                      @click="isPwd = !isPwd" />
                  </template>
                </q-input>
              </div>

              <div>
                <q-btn
                  label="Login"
                  type="button"
                  color="primary"
                  style="width: 100%; height: 40px"
                  @click="login()" />
                <q-btn
                  label="Accesso manuale"
                  type="button"
                  color="warning"
                  style="width: 100%; height: 40px; margin-top: 10px"
                  @click="manualLogin()" />
              </div>
            </q-card-section>
            <p
              class="text-caption"
              style="display: flex; justify-content: center"
              @click="$router.push('/subscriber')">
              Cambio subscriber
            </p>
            <!--<p
            class="text-caption"
            style="display: flex; justify-content: center"
          >
            Hai dimenticato la password?
            <span @click="$router.push('/subscriber')">Recupera</span>
          </p>-->
          </q-form>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, inject } from 'vue'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'
import moment from 'moment'

export default defineComponent({
  name: 'Login',
  setup() {
    const $q = useQuasar()
    const resetIdle = inject('resetIdle')
    return {
      showNotif(t, msg, time) {
        $q.notify({
          type: t,
          message: msg,
          position: 'top-right',
          timeout: time
        })
      },
      resetIdle
    }
  },
  data() {
    return {
      operators: [],
      operator: {
        username: '',
        password: '',
        subscriber: sessionStorage.getItem('subscriber')
      },
      isPwd: true,
      isSelected: false
    }
  },
  mounted() {},
  methods: {
    manualLogin() {
      api
        .post('/auth/login/manual', {
          ...this.operator,
          start_date: moment().format('DD/MM/YYYY HH:mm')
        })
        .then(response => {
          if (response.data?.status && response.data.status === 'pending') {
            this.showNotif('info', response.data['msg'], 5000)
            this.$router.push('/')
          } else {
            this.$store.commit('updateLoginStatus', true)
            api.post('/auth/access-token', this.operator).then(response => {
              sessionStorage.setItem('access-token', response.data.token)
            })
            sessionStorage.setItem('user', JSON.stringify(response.data))
            this.$store.commit('updateOperator', response.data)
            this.resetIdle()
            this.$router.push('/')
          }
        })
        .catch(err => {
          const errors = {
            404: 'Utente non trovato',
            401: 'Credenziali errate'
          }
          if (err.response.status in errors) {
            this.showNotif('negative', errors[err.response.status], 1000)
          } else {
            this.showNotif(
              'negative',
              err.response.data?.detail
                ? err.response.data.detail
                : err.response.data.description,
              1000
            )
          }
        })
    },
    login() {
      api
        .post('/auth/login', this.operator)
        .then(response => {
          api
            .post('/auth/access-token', this.operator)
            .then(response => {
              sessionStorage.setItem('access-token', response.data.token)
            })
            .then(() => {
              sessionStorage.setItem('user', JSON.stringify(response.data))
              this.$store.commit('updateOperator', response.data)
              this.$store.commit('updateLoginStatus', true)
              this.resetIdle()
              this.$router.push('/')
            })
            .catch(err => {
              this.showNotif(
                'negative',
                err.response.data?.detail
                  ? err.response.data.detail
                  : err.response.data.description,
                1000
              )
            })
        })
        .catch(err => {
          const errors = {
            404: 'Utente non trovato',
            401: 'Credenziali errate'
          }
          if (err.response.status in errors) {
            this.showNotif('negative', errors[err.response.status], 1000)
          } else {
            this.showNotif(
              'negative',
              err.response.data?.detail
                ? err.response.data.detail
                : err.response.data.description,
              1000
            )
          }
        })
    }
  }
})
</script>

<style>
.bg-image {
  background-image: linear-gradient(135deg, #019a29 0%, #85ffa6 100%);
}
[v-cloak] {
  display: none !important;
}
</style>
