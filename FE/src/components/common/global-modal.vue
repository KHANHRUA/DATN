<template>
  <el-dialog v-model="modal" class="modal-container" :style="`width: ${width}%`" :show-close="showClose">
    <template v-slot:header>
      <slot name="header"/>
    </template>
    <template v-slot:default>
      <slot name="default"/>
    </template>
    <template v-slot:footer>
      <div>
        <el-button v-if="!footer" @click="hide">Cancel</el-button>
        <el-button v-if="!footer" :type="type" @click="okClick">Confirm</el-button>
        <slot name="footer"/>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts">
export default {
  name: 'GlobalModal',
  props: {
    showClose: {
      type: Boolean,
      default: false
    },
    footer: {
      type: Boolean,
      default: false
    },
    width: {
      type: Number,
      default: 70
    },
    type: {
      type: String,
      default: 'primary'
    }
  },
  data() {
    return {
      modal: false
    }
  },
  created() {
  },
  methods:{
    show() {
      this.modal = true
    },
    hide() {
      this.modal = false
    },
    okClick() {
      this.$emit('submit')
    }
  }
}
</script>