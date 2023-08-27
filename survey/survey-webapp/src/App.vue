<template>
  <div class="survey">
    <header>
      <h1>Survey</h1>
    </header>
    <main>
      <div class="options">
        <label>
          <input type="radio" v-model="selectedOption" value="A">
          <div class="option">
            <TerrainVis
              :heightmap="require('@/assets/hgtelev_0_-22.269158650668658_145.64846199698434_20230813_134144.png')"
              :normalmap="require('@/assets/nrmelev_0_-22.269158650668658_145.64846199698434_20230813_134144.png')"
              :strength=10 />
            <span class="option-label">A</span>
          </div>
        </label>
        <label>
          <input type="radio" v-model="selectedOption" value="B">
          <div class="option">
            <TerrainVis
              :heightmap="require('@/assets/hgtelev_3_-27.30251610869659_134.17288977854216_20230813_134144.png')"
              :normalmap="require('@/assets/nrmelev_3_-27.30251610869659_134.17288977854216_20230813_134144.png')"
              :strength=10 />
            <span class="option-label">B</span>
          </div>
        </label>
      </div>
      <p class="selected-option">You selected: {{ selectedOption }}</p>
    </main>
  </div>
</template>

<script>
import TerrainVis from './components/Terrain-Vis.vue';

export default {
  name: 'OptionSelector',
  data() {
    return {
      selectedOption: 'left'
    }
  },
  methods: {
    selectLeft() {
      this.selectedOption = 'left';
    },
    selectRight() {
      this.selectedOption = 'right';
    }
  },
  components: {
    TerrainVis
  }
}
</script>

<style>
.survey {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: Arial, sans-serif;
  height: 100vh;
}

header {
  background-color: #333;
  color: white;
  padding: 10px;
  width: 100%;
  text-align: center;
}

h1 {
  margin: 0;
}

main {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.options {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 500px;
}

.option {
  position: relative;
  margin-bottom: 20px;
}

.option-label {
  position: absolute;
  bottom: 10px;
  left: 10px;
  color: white;
  font-size: 24px;
}

.selected-option {
  margin-top: 20px;
  font-size: 24px;
}
</style>