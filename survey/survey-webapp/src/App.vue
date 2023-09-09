<template>
  <div class="common-layout">
    <el-header justify="center" justify-content="center">
      <h1>Survey</h1>
    </el-header>
    <el-main>
      <el-row>
        <el-col :span="24" justify="center">
          <div :class="['option', { selected: selectedOption === 'A' }]">
            <TerrainVis
              :heightmap="require('@/assets/hgtelev_0_-22.269158650668658_145.64846199698434_20230813_134144.png')"
              :normalmap="require('@/assets/nrmelev_0_-22.269158650668658_145.64846199698434_20230813_134144.png')"
              :strength=10 />
          </div>
        </el-col>
        <el-col :span="24" justify="center">
          <div :class="['option', { selected: selectedOption === 'B' }]">
            <TerrainVis
              :heightmap="require('@/assets/hgtelev_3_-27.30251610869659_134.17288977854216_20230813_134144.png')"
              :normalmap="require('@/assets/nrmelev_3_-27.30251610869659_134.17288977854216_20230813_134144.png')"
              :strength=10 />
          </div>
        </el-col>
        <p class="selected-option">You selected: {{ selectedOption }}</p>
      </el-row>
    </el-main>
  </div>
</template>

<script>
import { ElHeader, ElMain, ElRow, ElCol } from 'element-plus';
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
    ElHeader,
    ElCol,
    ElRow,
    ElMain,
    TerrainVis,
  }
}
</script>