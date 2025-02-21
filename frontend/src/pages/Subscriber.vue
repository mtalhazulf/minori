<template>
  <q-layout v-cloak class="bg-image">
    <q-page-container>
      <q-page class="flex flex-center">
        <q-card class="bg-transparent no-border no-shadow">
          <q-item>
            <q-item-section avatar>
              <q-avatar
                size="130px"
                class="shadow-10"
                color="white"
                text-color="grey"
                font-size="160px"
                icon="person" />
            </q-item-section>

            <q-item-section class="text-white">
              <q-item-label class="q-pt-sm q-mb-sm" caption>
                <q-select
                  ref="name"
                  v-model="subscriber"
                  borderless
                  label="Subscriber"
                  :options="subscribers"
                  style="width: 250px"
                  behavior="menu"
                  option-value="companyName"
                  option-label="companyName"
                  dark
                  color="white"
                  @update:model-value="setValue($event)" />
              </q-item-label>
              <q-item-label></q-item-label>
            </q-item-section>
            <q-item-section side center>
              <q-btn
                :disable="subscriber === ''"
                round
                flat
                color="white"
                class="q-mt-lg bg-blue-5"
                icon="arrow_right_alt"
                @click="setSubscriber()"></q-btn>
            </q-item-section>
          </q-item>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { api } from 'src/boot/axios'
import { defineComponent } from 'vue'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'Subscriber',
  setup() {
    const $q = useQuasar()

    return {
      showNotif() {
        $q.notify({
          type: 'negative',
          message: 'Password errata!',
          position: 'top-right',
          timeout: 1000
        })
      }
    }
  },
  data() {
    return {
      operators: [],
      step: 1,
      subscriber: '',
      subscribers: [],
      img: 0,
      isPwd: true,
      isSelected: false
    }
  },
  mounted() {
    this.getSubscribers()
  },
  methods: {
    setValue(e) {
      this.isSelected = true
    },
    getSubscribers() {
      api.get('/auth/user/subscribers').then(response => {
        this.subscribers = response.data.filter(e => {
          if (e.username === 'admin' || e.username === 'superadmin') {
            return e
          }
        })
      })
    },
    setSubscriber() {
      sessionStorage.setItem('subscriber', this.subscriber.username)
      this.$router.push('/login')
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
