<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex flex-center" style="background: #f2f2f27a">
        <q-card :style="$q.screen.lt.sm ? { width: '80%' } : { width: '30%' }">
          <q-card-section>
            <div class="text-center q-pt-lg">
              <div class="col text-h6 ellipsis">Cambio Password</div>
            </div>
          </q-card-section>
          <q-form class="q-gutter-md">
            <q-card-section>
              <div>
                <q-input
                  v-model="operator.password"
                  filled
                  class="q-my-md"
                  :type="isPwd ? 'password' : 'text'"
                  placeholder="Password"
                  ><template #append>
                    <q-icon
                      :name="isPwd ? 'visibility_off' : 'visibility'"
                      class="cursor-pointer"
                      @click="isPwd = !isPwd" />
                  </template>
                </q-input>
                <q-input
                  v-model="operator.new_password"
                  filled
                  class="q-my-md"
                  :type="isNewPwd ? 'password' : 'text'"
                  placeholder="Nuova Password">
                  <template #append>
                    <q-icon
                      :name="isNewPwd ? 'visibility_off' : 'visibility'"
                      class="cursor-pointer"
                      @click="isNewPwd = !isNewPwd" />
                  </template>
                </q-input>
              </div>

              <div>
                <q-btn
                  label="Effettua cambio"
                  type="button"
                  color="primary"
                  style="width: 100%; height: 40px"
                  @click="changePassword()" />
              </div>
            </q-card-section>
          </q-form>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'ChangePassword',
  setup() {
    const $q = useQuasar()

    return {
      showNotif(t, msg, time) {
        $q.notify({
          type: t,
          message: msg,
          position: 'top-right',
          timeout: time
        })
      }
    }
  },
  data() {
    return {
      operator: {
        password: '',
        new_password: ''
      },
      isPwd: true,
      isNewPwd: true,
      isSelected: false
    }
  },
  mounted() {},
  methods: {
    validate(op) {
      const fields = { password: 'Password', new_password: 'Nuova Password' }
      let isValid = true
      Object.keys(op).forEach(el => {
        if (op[el].trim() === '') {
          this.showNotif('warning', 'Compilare il campo ' + fields[el])
          isValid = false
        }
      })
      return isValid
    },
    changePassword() {
      if (this.validate(this.operator)) {
        api
          .put('/auth/user/change-password', this.operator)
          .then(response => {
            this.showNotif('positive', 'Password cambiata correttamente')
            this.$router.push('/')
          })
          .catch(err => {
            this.showNotif('negative', 'Errore durante il cambio password')
          })
      }
    }
  }
})
</script>

<style>
[v-cloak] {
  display: none !important;
}
</style>
