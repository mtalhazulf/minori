<!-- eslint-disable vue/no-v-html -->
<!-- UserIncentives.vue -->
<template>
  <q-page class="q-mx-xl">
    <div class="row">
      <Heading :title="'I Miei Incentivi'" />
    </div>

    <q-expansion-item
      v-model="showFilters"
      group="filters"
      switch-toggle-side
      dense
      class="filter-panel q-mb-md">
      <template #header>
        <div class="filter-header full-width cursor-pointer">
          <q-icon name="filter_list" color="primary" size="24px" />
          <div class="text-h6 text-primary q-my-none">Filtri</div>
          <q-space />
          <div class="text-caption text-grey">
            <transition name="filter-count">
              <span v-if="hasActiveFilters">
                {{ activeFilterCount }} filtri attivi
                <q-btn
                  flat
                  dense
                  round
                  color="grey"
                  icon="clear_all"
                  size="sm"
                  @click.stop="clearAllFilters">
                  <q-tooltip>Cancella tutti i filtri</q-tooltip>
                </q-btn>
              </span>
            </transition>
          </div>
          <q-icon
            :name="showFilters ? 'expand_less' : 'expand_more'"
            color="primary"
            size="24px"
            class="q-ml-sm transition-transform"
            :class="{ 'rotate-180': !showFilters }" />
        </div>
      </template>

      <q-card>
        <q-card-section>
          <div class="row q-col-gutter-md">
            <div class="col-12 col-sm-6 col-md-4">
              <div class="text-subtitle2 q-mb-sm">Settore attività</div>
              <q-select
                v-model="selectedSectors"
                :options="sectorOptions"
                multiple
                outlined
                dense
                options-dense
                use-chips
                input-debounce="0"
                behavior="menu"
                class="custom-select"
                popup-content-class="custom-select-popup"
                hide-dropdown-icon
                clearable
                :style="{ minHeight: '56px', maxHeight: '56px' }"
                @update:model-value="onSelectInput($event, 'sectors')">
                <template #append>
                  <q-icon name="expand_more" class="cursor-pointer" />
                </template>
                <template #selected-item="scope">
                  <q-chip
                    removable
                    dense
                    color="primary"
                    text-color="white"
                    class="select-chip"
                    @remove="scope.removeAtIndex(scope.index)">
                    {{ scope.opt.label }}
                  </q-chip>
                </template>
              </q-select>
            </div>

            <div class="col-12 col-sm-6 col-md-4">
              <div class="text-subtitle2 q-mb-sm">Regioni</div>
              <q-select
                v-model="selectedRegions"
                :options="regionOptions"
                multiple
                outlined
                dense
                options-dense
                use-chips
                input-debounce="0"
                behavior="menu"
                class="custom-select"
                popup-content-class="custom-select-popup"
                hide-dropdown-icon
                clearable
                :style="{ minHeight: '56px', maxHeight: '56px' }"
                @update:model-value="onSelectInput($event, 'regions')">
                <template #append>
                  <q-icon name="expand_more" class="cursor-pointer" />
                </template>
                <template #selected-item="scope">
                  <q-chip
                    removable
                    dense
                    color="primary"
                    text-color="white"
                    class="select-chip"
                    @remove="scope.removeAtIndex(scope.index)">
                    {{ scope.opt.label }}
                  </q-chip>
                </template>
              </q-select>
            </div>

            <div class="col-12 col-sm-6 col-md-4">
              <div class="text-subtitle2 q-mb-sm">Forma di supporto</div>
              <q-select
                v-model="selectedSupportForms"
                :options="supportFormOptions"
                multiple
                outlined
                dense
                options-dense
                use-chips
                input-debounce="0"
                behavior="menu"
                class="custom-select"
                popup-content-class="custom-select-popup"
                hide-dropdown-icon
                clearable
                :style="{ minHeight: '56px', maxHeight: '56px' }"
                @update:model-value="onSelectInput($event, 'supportForms')">
                <template #append>
                  <q-icon name="expand_more" class="cursor-pointer" />
                </template>
                <template #selected-item="scope">
                  <q-chip
                    removable
                    dense
                    color="primary"
                    text-color="white"
                    class="select-chip"
                    @remove="scope.removeAtIndex(scope.index)">
                    {{ scope.opt.label }}
                  </q-chip>
                </template>
              </q-select>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-expansion-item>

    <div class="row q-mb-md">
      <div class="col-12">
        <q-table
          v-model:pagination="pagination"
          class="user-incentives-table full-width"
          :rows="filteredIncentives"
          :columns="columns"
          row-key="id"
          :loading="loading"
          flat
          bordered
          :rows-per-page-options="[5, 8, 10, 15, 25, 50]">
          <template #loading>
            <q-inner-loading showing color="primary">
              <q-spinner-dots size="50px" color="primary" />
            </q-inner-loading>
          </template>

          <template #body-cell-title="props">
            <q-td>
              <q-tooltip>{{ props.row.title }}</q-tooltip>
              {{ props.value }}
            </q-td>
          </template>

          <template #body-cell-activity_sector="props">
            <q-td class="text-left">
              <q-tooltip>{{ props.value }}</q-tooltip>
              {{ props.value }}
            </q-td>
          </template>

          <template #body-cell-regions="props">
            <q-td class="text-left">
              <q-tooltip>{{ props.value }}</q-tooltip>
              {{ props.value }}
            </q-td>
          </template>

          <template #body-cell-categories="props">
            <q-td class="text-left">
              <q-chip
                v-for="category in props.row.categories"
                :key="category"
                color="primary"
                text-color="white"
                size="sm"
                class="q-ma-xs">
                {{ category }}
              </q-chip>
            </q-td>
          </template>

          <template #body-cell-status="props">
            <q-td class="text-left">
              <q-chip
                :color="props.value === 'In Arrivo' ? 'orange' : 'green'"
                text-color="white"
                size="sm">
                {{ props.value }}
              </q-chip>
            </q-td>
          </template>

          <template #body-cell-dates="props">
            <q-td class="text-left">
              {{ props.value }}
            </q-td>
          </template>

          <template #body-cell-actions="props">
            <q-td class="text-center">
              <q-btn
                flat
                round
                dense
                color="primary"
                icon="analytics"
                @click="openAnalyzeDialog(props.row)">
                <q-tooltip>Analizza</q-tooltip>
              </q-btn>
              <q-btn
                flat
                round
                dense
                color="primary"
                icon="open_in_new"
                class="q-mx-sm"
                @click="openUrl(props.row.link)">
                <q-tooltip>Apri link</q-tooltip>
              </q-btn>
              <q-btn
                flat
                round
                dense
                color="warning"
                icon="edit"
                class="q-mx-sm"
                @click="editIncentive(props.row)">
                <q-tooltip>Modifica</q-tooltip>
              </q-btn>
              <q-btn
                flat
                round
                dense
                color="negative"
                icon="delete"
                class="q-mx-sm"
                @click="confirmDelete(props.row)">
                <q-tooltip>Elimina</q-tooltip>
              </q-btn>
            </q-td>
          </template>
        </q-table>
      </div>
    </div>

    <!-- Edit Dialog -->
    <q-dialog v-model="editDialog.show" persistent>
      <q-card style="min-width: 500px">
        <q-card-section>
          <div class="text-h6">Modifica Incentivo</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            v-model="editDialog.form.title"
            label="Titolo"
            outlined
            dense
            :loading="editDialog.processing"
            :disable="editDialog.processing"
            class="q-mb-md" />

          <div class="row q-col-gutter-md">
            <div class="col-6">
              <q-input
                v-model="editDialog.form.open_date"
                label="Data Apertura"
                outlined
                dense
                type="datetime-local"
                :loading="editDialog.processing"
                :disable="editDialog.processing"
                class="q-mb-md" />
            </div>
            <div class="col-6">
              <q-input
                v-model="editDialog.form.close_date"
                label="Data Chiusura"
                outlined
                dense
                type="datetime-local"
                :loading="editDialog.processing"
                :disable="editDialog.processing"
                class="q-mb-md" />
            </div>
          </div>

          <q-select
            v-model="editDialog.form.activity_sector"
            label="Settore attività"
            :options="sectorOptions"
            multiple
            outlined
            dense
            options-dense
            use-chips
            input-debounce="0"
            behavior="menu"
            class="custom-select q-mb-md"
            popup-content-class="custom-select-popup"
            hide-dropdown-icon
            :loading="editDialog.processing"
            :disable="editDialog.processing"
            :style="{ minHeight: '56px', maxHeight: '56px' }">
            <template #append>
              <q-icon name="expand_more" class="cursor-pointer" />
            </template>
            <template #selected-item="{ opt }">
              <q-chip
                dense
                color="primary"
                text-color="white"
                class="select-chip">
                {{ opt.label }}
              </q-chip>
            </template>
          </q-select>

          <q-select
            v-model="editDialog.form.regions"
            label="Regioni"
            :options="regionOptions"
            multiple
            outlined
            dense
            options-dense
            use-chips
            input-debounce="0"
            behavior="menu"
            class="custom-select q-mb-md"
            popup-content-class="custom-select-popup"
            hide-dropdown-icon
            :loading="editDialog.processing"
            :disable="editDialog.processing"
            :style="{ minHeight: '56px', maxHeight: '56px' }">
            <template #append>
              <q-icon name="expand_more" class="cursor-pointer" />
            </template>
            <template #selected-item="{ opt }">
              <q-chip
                dense
                color="primary"
                text-color="white"
                class="select-chip">
                {{ opt.label }}
              </q-chip>
            </template>
          </q-select>

          <q-select
            v-model="editDialog.form.support_form"
            label="Forma di supporto"
            :options="supportFormOptions"
            multiple
            outlined
            dense
            options-dense
            use-chips
            input-debounce="0"
            behavior="menu"
            class="custom-select q-mb-md"
            popup-content-class="custom-select-popup"
            hide-dropdown-icon
            :loading="editDialog.processing"
            :disable="editDialog.processing"
            :style="{ minHeight: '56px', maxHeight: '56px' }">
            <template #append>
              <q-icon name="expand_more" class="cursor-pointer" />
            </template>
            <template #selected-item="{ opt }">
              <q-chip
                dense
                color="primary"
                text-color="white"
                class="select-chip">
                {{ opt.label }}
              </q-chip>
            </template>
          </q-select>

          <q-select
            v-model="editDialog.form.categories"
            label="Categorie"
            :options="categoryOptions"
            multiple
            outlined
            dense
            options-dense
            use-chips
            :loading="editDialog.processing"
            :disable="editDialog.processing"
            class="q-mb-md">
            <template #selected-item="{ opt }">
              <q-chip
                dense
                color="primary"
                text-color="white"
                class="select-chip">
                {{ opt }}
              </q-chip>
            </template>
          </q-select>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn
            v-close-popup
            flat
            label="Annulla"
            :disable="editDialog.processing" />
          <q-btn
            flat
            label="Salva"
            :loading="editDialog.processing"
            @click="updateIncentive" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="deleteDialog.show" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Elimina Incentivo</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="text-subtitle1 q-mb-md">
            {{ deleteDialog.incentive?.title }}
          </div>
          <div class="text-body2">
            Sei sicuro di voler eliminare questo incentivo?
          </div>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn
            v-close-popup
            flat
            label="Annulla"
            :disable="deleteDialog.processing" />
          <q-btn
            flat
            label="Elimina"
            color="negative"
            :loading="deleteDialog.processing"
            @click="deleteIncentive" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Analyze Dialog -->
    <q-dialog v-model="analyzeDialog.show" persistent>
      <q-card style="min-width: 500px; max-width: 80vw; width: 800px">
        <q-card-section class="row items-center">
          <div class="text-h6">Analisi Incentivo</div>
          <q-space />
          <q-btn v-close-popup icon="close" flat round dense />
          <q-btn
            v-if="hasCachedAnalysis"
            icon="delete"
            flat
            round
            dense
            @click="clearAnalysisCache" />
        </q-card-section>

        <q-card-section>
          <div v-if="analyzeDialog.processing" class="text-center q-pa-md">
            <q-spinner color="primary" size="3em" />
            <div class="text-body1 q-mt-sm">
              {{
                analyzeDialog.currentStep === 'scraping'
                  ? 'Scraping della pagina Bandi in corso...'
                  : 'Analisi del testo in corso...'
              }}
            </div>
          </div>

          <div v-else-if="analyzeDialog.error" class="text-negative q-mb-md">
            <div class="text-h6 q-mb-sm">
              {{
                analyzeDialog.currentStep === 'scraping'
                  ? 'Scraping Bandi Fallito'
                  : 'Analisi del Testo Fallita'
              }}
            </div>
            {{ analyzeDialog.error }}
          </div>

          <div
            v-else-if="!analyzeDialog.analysis && !hasCachedAnalysis"
            class="text-center q-pa-md">
            <div class="text-body1 q-mb-sm">
              L'analisi può richiedere fino a 1 minuto.
            </div>
            <div class="text-caption text-grey-7">
              Puoi chiudere questa finestra e tornare più tardi per vedere i
              risultati.
            </div>
          </div>

          <div v-else-if="analyzeDialog.analysis" class="analysis-content">
            <div class="analysis-text" v-html="renderedAnalysis"></div>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn
            v-close-popup
            flat
            label="CHIUDI"
            :disable="analyzeDialog.processing" />
          <q-btn
            v-if="!analyzeDialog.analysis && !analyzeDialog.processing"
            color="primary"
            label="ANALIZZA"
            :loading="analyzeDialog.processing"
            @click="analyzeIncentive" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { api } from 'src/boot/axios'
import Heading from 'components/Heading.vue'
import { marked } from 'marked'
import { SUPPORT_FORM_OPTIONS, getRegionName } from 'src/const/incentivi'

import { _regions, _sectors } from 'src/const/incentivi'

export default {
  name: 'UserIncentives',
  components: {
    Heading
  },
  data() {
    return {
      loading: false,
      incentives: [],
      showFilters: false,
      selectedSectors: [],
      selectedRegions: [],
      selectedSupportForms: [],
      pagination: {
        sortBy: 'title',
        descending: false,
        page: 1,
        rowsPerPage: 10
      },
      editDialog: {
        show: false,
        processing: false,
        incentive: null,
        form: {
          id: '',
          title: '',
          link: '',
          activity_sector: [],
          categories: [],
          regions: [],
          scopes: [],
          support_form: [],
          granted_costs: [],
          open_date: '',
          close_date: '',
          status: '',
          user_id: '',
          last_updated: ''
        }
      },
      deleteDialog: {
        show: false,
        processing: false,
        incentive: null
      },
      analyzeDialog: {
        show: false,
        processing: false,
        error: null,
        analysis: null,
        incentive: null,
        currentStep: null
      },
      columns: [
        {
          name: 'title',
          required: true,
          label: 'Titolo',
          align: 'left',
          field: row => this.truncateText(row.title, 50),
          sortable: true
        },
        {
          name: 'regions',
          align: 'left',
          label: 'Regioni',
          field: row =>
            row.regions?.map(code => getRegionName(code)).join(', ') || '',
          sortable: true
        },
        {
          name: 'categories',
          align: 'left',
          label: 'Categorie',
          field: row => row.categories?.join(', ') || '',
          sortable: true
        },
        {
          name: 'status',
          align: 'left',
          label: 'Stato',
          field: 'status',
          sortable: true
        },
        {
          name: 'dates',
          align: 'left',
          label: 'Date',
          field: row => {
            const openDate = row.open_date
              ? new Date(row.open_date).toLocaleDateString()
              : '-'
            const closeDate = row.close_date
              ? new Date(row.close_date).toLocaleDateString()
              : '-'
            return `${openDate} - ${closeDate}`
          },
          sortable: true
        },
        {
          name: 'actions',
          align: 'center',
          label: 'Azioni',
          field: row => row
        }
      ],
      sectors: _sectors,
      regions: _regions,
      supportForms: SUPPORT_FORM_OPTIONS,
      grantedCostOptions: []
    }
  },
  computed: {
    sectorOptions() {
      return Object.entries(_sectors).map(([label, value]) => ({
        label,
        value
      }))
    },
    regionOptions() {
      return Object.entries(_regions).map(([label, value]) => ({
        label,
        value
      }))
    },
    supportFormOptions() {
      return Object.entries(SUPPORT_FORM_OPTIONS).map(([value, label]) => ({
        label,
        value
      }))
    },
    filteredIncentives() {
      return this.incentives.filter(incentive => {
        const sectorMatch =
          this.selectedSectors.length === 0 ||
          this.selectedSectors.some(selected => {
            const matches = incentive.activity_sector.includes(selected.value)
            return matches
          })
        const regionMatch =
          this.selectedRegions.length === 0 ||
          this.selectedRegions.some(selected => {
            const matches = incentive.regions.includes(selected.value)
            return matches
          })

        const supportFormMatch =
          this.selectedSupportForms.length === 0 ||
          this.selectedSupportForms.some(selected => {
            const matches = incentive.support_form.includes(selected.value)
            return matches
          })

        const finalMatch = sectorMatch && regionMatch && supportFormMatch

        return finalMatch
      })
    },
    hasActiveFilters() {
      return (
        this.selectedSectors.length > 0 ||
        this.selectedRegions.length > 0 ||
        this.selectedSupportForms.length > 0
      )
    },
    activeFilterCount() {
      return (
        this.selectedSectors.length +
        this.selectedRegions.length +
        this.selectedSupportForms.length
      )
    },
    renderedAnalysis() {
      if (!this.analyzeDialog.analysis) return ''
      marked.setOptions({
        gfm: true,
        breaks: true,
        headerIds: false,
        mangle: false,
        pedantic: false,
        sanitize: false,
        smartLists: true,
        smartypants: false,
        langPrefix: 'language-'
      })
      return marked(this.analyzeDialog.analysis)
    },
    hasCachedAnalysis() {
      return (
        this.analyzeDialog.incentive?.link &&
        localStorage.getItem(this.analyzeDialog.incentive.link) !== null
      )
    }
  },
  mounted() {
    this.fetchUserIncentives()
  },
  methods: {
    async fetchUserIncentives() {
      this.loading = true
      try {
        const response = await api.get('scrapper/incentives/all')
        if (response.data && response.data.success) {
          this.incentives = (response.data.data || []).map(incentive => {
            const processed = {
              ...incentive,
              activity_sector: Array.isArray(incentive.activity_sector)
                ? incentive.activity_sector
                : incentive.activity_sector
                ? [incentive.activity_sector]
                : [],
              regions: Array.isArray(incentive.regions)
                ? incentive.regions
                : incentive.regions
                ? [incentive.regions]
                : [],
              support_form: Array.isArray(incentive.support_form)
                ? incentive.support_form
                : incentive.support_form
                ? [incentive.support_form]
                : [],
              status: this.calculateStatus(incentive)
            }
            return processed
          })
        } else {
          this.incentives = []
          throw new Error('Invalid response format')
        }
      } catch (error) {
        this.$q.notify({
          type: 'negative',
          message: 'Errore nel caricamento degli incentivi',
          position: 'top',
          timeout: 3000
        })
        this.incentives = []
      } finally {
        this.loading = false
      }
    },

    onSelectInput(value, type) {
      switch (type) {
        case 'sectors':
          this.selectedSectors = value || []
          break
        case 'regions':
          this.selectedRegions = value || []
          break
        case 'supportForms':
          this.selectedSupportForms = value || []
          break
      }
    },

    clearAllFilters() {
      this.selectedSectors = []
      this.selectedRegions = []
      this.selectedSupportForms = []
    },

    editIncentive(incentive) {
      this.editDialog.incentive = incentive
      this.editDialog.form = {
        id: incentive.id,
        title: incentive.title,
        link: incentive.link,
        activity_sector: incentive.activity_sector
          .map(id => this.sectorOptions.find(opt => opt.value === id))
          .filter(Boolean),
        categories: incentive.categories || [],
        regions: incentive.regions
          .map(id => this.regionOptions.find(opt => opt.value === id))
          .filter(Boolean),
        scopes: incentive.scopes || [],
        support_form: incentive.support_form
          .map(id => this.supportFormOptions.find(opt => opt.value === id))
          .filter(Boolean),
        granted_costs: incentive.granted_costs || [],
        open_date: incentive.open_date || '',
        close_date: incentive.close_date || '',
        status: incentive.status || '',
        user_id: incentive.user_id || '',
        last_updated: incentive.last_updated || ''
      }
      this.editDialog.show = true
    },

    async updateIncentive() {
      this.editDialog.processing = true
      try {
        const updatedData = {
          ...this.editDialog.form,
          activity_sector: this.editDialog.form.activity_sector.map(
            opt => opt.value
          ),
          regions: this.editDialog.form.regions.map(opt => opt.value),
          support_form: this.editDialog.form.support_form.map(opt => opt.value),
          last_updated: new Date().toISOString()
        }

        const response = await api.put(
          `scrapper/incentives/${this.editDialog.form.id}`,
          updatedData
        )

        this.$q.notify({
          type: 'positive',
          message: 'Incentivo aggiornato con successo',
          position: 'top',
          timeout: 3000
        })
        const index = this.incentives.findIndex(
          i => i.id === this.editDialog.form.id
        )
        if (index !== -1) {
          this.incentives[index] = {
            ...this.incentives[index],
            ...updatedData,
            status: this.calculateStatus(updatedData)
          }
        }

        this.editDialog.show = false
      } catch (error) {
        this.$q.notify({
          type: 'negative',
          message: "Errore durante l'aggiornamento dell'incentivo",
          position: 'top',
          timeout: 3000
        })
      } finally {
        this.editDialog.processing = false
      }
    },

    confirmDelete(incentive) {
      this.deleteDialog.incentive = incentive
      this.deleteDialog.show = true
    },

    async deleteIncentive() {
      if (!this.deleteDialog.incentive) return

      this.deleteDialog.processing = true
      try {
        await api.delete(
          `scrapper/incentives/${this.deleteDialog.incentive.id}`
        )

        this.$q.notify({
          type: 'positive',
          message: 'Incentivo eliminato con successo',
          position: 'top'
        })

        this.deleteDialog.show = false
        this.fetchUserIncentives()
      } catch (error) {
        let errorMessage = "Errore durante l'eliminazione dell'incentivo"

        if (error.response?.status === 404) {
          errorMessage = 'Incentivo non trovato'
        }

        this.$q.notify({
          type: 'negative',
          message: errorMessage,
          position: 'top'
        })
      } finally {
        this.deleteDialog.processing = false
      }
    },

    openAnalyzeDialog(incentive) {
      this.analyzeDialog.incentive = incentive
      this.analyzeDialog.error = null
      this.analyzeDialog.processing = false
      this.analyzeDialog.analysis = ''
      this.analyzeDialog.currentStep = null
      const cachedAnalysis = localStorage.getItem(incentive.link)
      if (cachedAnalysis) {
        this.analyzeDialog.analysis = cachedAnalysis
      }

      this.analyzeDialog.show = true
    },

    async analyzeIncentive() {
      this.analyzeDialog.processing = true
      this.analyzeDialog.error = null
      this.analyzeDialog.currentStep = 'scraping'
      const cachedAnalysis = localStorage.getItem(
        this.analyzeDialog.incentive.link
      )
      if (cachedAnalysis) {
        this.analyzeDialog.analysis = cachedAnalysis
        this.analyzeDialog.processing = false
        return
      }
      try {
        // Step 1: Scrape the text from the URL
        const scrapeResponse = await api.post('scrapper/analyze', {
          url:
            'https://www.incentivi.gov.it' + this.analyzeDialog.incentive.link
        })

        if (!scrapeResponse.data?.success) {
          throw new Error("Errore durante l'estrazione del testo")
        }

        // Step 2: Analyze the scraped text
        this.analyzeDialog.currentStep = 'analyzing'
        const analysisResponse = await api.post('scrapper/analyze-text', {
          text: scrapeResponse.data.text
        })

        if (analysisResponse.data?.success) {
          this.analyzeDialog.analysis = analysisResponse.data.analysis
          localStorage.setItem(
            this.analyzeDialog.incentive.link,
            analysisResponse.data.analysis
          )
        } else {
          throw new Error("Errore durante l'analisi dell'incentivo")
        }
      } catch (error) {
        console.error('Error analyzing incentive:', error)
        this.analyzeDialog.error =
          error.response?.data?.error ||
          error.message ||
          "Errore durante l'analisi dell'incentivo"
      } finally {
        this.analyzeDialog.processing = false
      }
    },

    clearAnalysisCache() {
      if (this.analyzeDialog.incentive?.link) {
        localStorage.removeItem(this.analyzeDialog.incentive.link)
        this.analyzeDialog.analysis = ''
        this.$q.notify({
          type: 'positive',
          message: 'Cache analisi cancellata',
          position: 'top-right',
          timeout: 2000
        })
      }
    },

    calculateStatus(row) {
      const now = new Date()
      const openDate = row.open_date ? new Date(row.open_date) : null
      const closeDate = row.close_date ? new Date(row.close_date) : null

      if (!openDate && !closeDate) return 'N/A'
      if (openDate && now < openDate) return 'In Arrivo'
      if (closeDate && now > closeDate) return 'Scaduto'
      return 'Attivo'
    },

    getStatusColor(status) {
      switch (status) {
        case 'Attivo':
          return 'positive'
        case 'In Arrivo':
          return 'warning'
        case 'Scaduto':
          return 'negative'
        default:
          return 'grey'
      }
    },

    truncateText(text, length = 50) {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    },

    openUrl(url) {
      const link = 'https://www.incentivi.gov.it'
      if (url) {
        window.open(link + url, '_blank')
      }
    },

    formatDateForInput(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toISOString().slice(0, 16)
    }
  }
}
</script>

<style scoped>
.user-incentives-table {
  background: white;
}

:deep(.q-table__container) {
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

:deep(.q-table__card) {
  border-radius: 8px;
}

:deep(.q-table thead tr) {
  height: 48px;
  background-color: #f5f5f5;
}

:deep(.q-table tbody tr:hover) {
  background-color: #f5f5f5;
}

:deep(.q-table tbody td) {
  height: 52px;
}

:deep(.q-table th) {
  font-weight: 500;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.85);
  padding: 8px 16px;
}

:deep(.q-table td) {
  font-size: 13px;
  color: rgba(0, 0, 0, 0.65);
  padding: 8px 16px;
}

:deep(.q-table__title) {
  font-size: 16px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
}

:deep(.q-table__bottom) {
  border-top: 1px solid rgba(0, 0, 0, 0.12);
}

:deep(.q-table__bottom .q-table__control) {
  font-size: 13px;
}

:deep(.q-table__grid-content) {
  min-height: 100px;
}

/* Column specific widths */
:deep(.q-table td:nth-child(1)),
:deep(.q-table th:nth-child(1)) {
  width: 35%;
}

:deep(.q-table td:nth-child(2)),
:deep(.q-table th:nth-child(2)) {
  width: 15%;
}

:deep(.q-table td:nth-child(3)),
:deep(.q-table th:nth-child(3)) {
  width: 15%;
}

:deep(.q-table td:nth-child(4)),
:deep(.q-table th:nth-child(4)) {
  width: 10%;
}

:deep(.q-table td:nth-child(5)),
:deep(.q-table th:nth-child(5)) {
  width: 15%;
}

:deep(.q-table td:nth-child(6)),
:deep(.q-table th:nth-child(6)) {
  width: 10%;
}

.catalogo-table {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 16px;
}

:deep(.q-table__container) {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

:deep(.q-table__card) {
  border-radius: 8px;
}

:deep(.q-table thead tr) {
  height: 48px;
}

:deep(.q-table tbody td) {
  height: 52px;
}

:deep(.q-table th) {
  font-weight: 500;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.85);
}

:deep(.q-table td) {
  font-size: 13px;
  color: rgba(0, 0, 0, 0.65);
}

.custom-select {
  width: 100%;
}

.custom-select :deep(.q-field__control) {
  height: 56px;
  padding: 0 12px;
}

.custom-select :deep(.q-field__control-container) {
  padding-top: 4px;
  padding-bottom: 4px;
  overflow-y: auto;
  max-height: 56px;
  scrollbar-width: thin;
}

.custom-select :deep(.q-field__control-container::-webkit-scrollbar) {
  width: 4px;
}

.custom-select :deep(.q-field__control-container::-webkit-scrollbar-track) {
  background: transparent;
}

.custom-select :deep(.q-field__control-container::-webkit-scrollbar-thumb) {
  background: #ddd;
  border-radius: 4px;
}

.custom-select
  :deep(.q-field__control-container::-webkit-scrollbar-thumb:hover) {
  background: #ccc;
}

.select-chip {
  margin: 2px;
  max-width: calc(100% - 4px);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

:deep(.custom-select-popup) {
  max-height: 300px;
}

:deep(.q-menu) {
  max-width: none !important;
  min-width: 200px !important;
}

:deep(.q-virtual-scroll__content) {
  padding: 4px 0;
}

:deep(.q-item) {
  min-height: 40px;
  padding: 8px 12px;
}

:deep(.q-item:hover) {
  background: rgba(0, 0, 0, 0.03);
}

:deep(.q-checkbox) {
  padding: 0;
  margin-left: 8px;
}

.filter-panel :deep(.q-card) {
  padding: 16px;
}

.filter-panel :deep(.q-card__section) {
  padding: 0;
}

.text-subtitle2 {
  margin-bottom: 8px;
  font-size: 14px;
}

.filter-title-column {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.filter-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  transition: background-color 0.3s ease;
}

.filter-header:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.filter-panel {
  background: white;
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
}

.filter-panel :deep(.q-expansion-item__container) {
  border: 1px solid #e0e0e0;
  transition: border-color 0.3s ease;
}

.filter-panel :deep(.q-expansion-item__container:hover) {
  border-color: var(--q-primary);
}

.transition-transform {
  transition: transform 0.3s ease;
}

.rotate-180 {
  transform: rotate(180deg);
}

:deep(.q-field--outlined .q-field__control) {
  border-radius: 8px;
  border-color: #e0e0e0;
  transition: border-color 0.3s ease;
}

:deep(.q-field--outlined .q-field__control:hover) {
  border-color: var(--q-primary);
}

:deep(.q-field--focused .q-field__control) {
  border-color: var(--q-primary);
  border-width: 2px;
}

:deep(.q-field__label) {
  font-size: 14px;
  color: #666;
}

.analysis-content {
  max-height: 70vh;
  overflow-y: auto;
  padding: 16px;
}

.analysis-text {
  line-height: 1.6;
  font-size: 14px;
  color: #2c3e50;
}

.analysis-text :deep(h1),
.analysis-text :deep(h2) {
  font-weight: 600;
  margin: 16px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #eaecef;
}

.analysis-text :deep(h1) {
  font-size: 24px;
}

.analysis-text :deep(h2) {
  font-size: 20px;
}

.analysis-text :deep(h3) {
  font-size: 18px;
  font-weight: 600;
  margin: 16px 0;
}

.analysis-text :deep(p) {
  margin: 12px 0;
  line-height: 1.7;
}

.analysis-text :deep(ul),
.analysis-text :deep(ol) {
  padding-left: 24px;
  margin: 12px 0;
}

.analysis-text :deep(li) {
  margin: 8px 0;
}

.analysis-text :deep(pre) {
  background-color: #f6f8fa;
  border-radius: 6px;
  padding: 16px;
  overflow: auto;
  margin: 16px 0;
  font-family: monospace;
}

.analysis-text :deep(code) {
  background-color: #f6f8fa;
  padding: 3px 6px;
  border-radius: 3px;
  font-family: monospace;
}

.analysis-text :deep(blockquote) {
  margin: 16px 0;
  padding: 0 16px;
  color: #6a737d;
  border-left: 4px solid #dfe2e5;
}

.analysis-text :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
}

.analysis-text :deep(table th),
.analysis-text :deep(table td) {
  border: 1px solid #dfe2e5;
  padding: 8px 12px;
  text-align: left;
}

.analysis-text :deep(table th) {
  background-color: #f6f8fa;
  font-weight: 600;
}

.analysis-text :deep(table tr:nth-child(2n)) {
  background-color: #f8f9fa;
}
</style>
