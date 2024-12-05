<template>
  <global-modal ref="editModal">
    <template v-slot:header>
      <div class="header-modal">
        Edit information
      </div>
    </template>
    <template v-slot:default>
      <el-form :model="form" :rules="rules">
        <el-upload ref="uploadImage" v-model:file-list="form.fileList" accept=".jpg,.jpeg,.png,.gif" :on-error="error" :on-success="success" :before-upload="beforeUpload" :file-size-limit="1024*1024*5" :on-exceed="onExceed" action="http://localhost:5000/api/user/upload-image" list-type="picture-card" draggable="true" :limit="1">
          <el-icon>
            <Plus/>
          </el-icon>
          <template #file="{ file }">
            <div>
              <img :src="file.url" alt="" class="el-upload-list__item-thumbnail"/>
              <span class="el-upload-list__item-actions">
                  <span
                      class="el-upload-list__item-preview"
                      @click="handlePictureCardPreview(file)"
                  >
                    <el-icon>
                      <zoom-in/>
                    </el-icon>
                  </span>
                  <span
                      class="el-upload-list__item-delete"
                      @click="handleRemove(file)"
                  >
                    <el-icon>
                      <Delete/>
                    </el-icon>
                  </span>
                </span>
            </div>
          </template>
        </el-upload>
        <br/>
        <el-row :gutter="20">
          <el-col :span="24" :md="12">
            <el-form-item label="Name" prop="name" label-position="top">
              <el-input v-model="form.name" placeholder="Type your name"/>
            </el-form-item>
          </el-col>
          <el-col :span="24" :md="6">
            <el-form-item label="Class" prop="class" label-position="top">
              <el-input disabled placeholder="class name" v-model="form.class_name"/>
            </el-form-item>
          </el-col>
          <el-col :span="12" :md="6">
            <el-form-item label="Age" prop="age" label-position="top">
              <el-input v-model="form.age" placeholder="Type your age"/>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <el-dialog v-model="dialogVisible" class="preview">
        <img :src="dialogImageUrl" alt="Preview Image" w-full/>
      </el-dialog>
    </template>
  </global-modal>
</template>

<script lang="ts">
import {Delete, Plus, ZoomIn} from "@element-plus/icons-vue";
import GlobalModal from "@/components/common/global-modal.vue";
import type {UploadFile} from "element-plus";
import {ROLES} from "@/utils/constant";
import UserService from "@/service/user-api/api";

export default {
  name: 'EditInformation',
  components: {GlobalModal, ZoomIn, Plus, Delete},
  data(){
    return{
      form: {
        name: '',
        age: null,
        role: 'student',
        face_image: '',
        class_id: null,
        fileList: [],
      },
      dialogVisible: false,
      dialogImageUrl: "",
      rules: {},
    }
  },
  methods: {
    show(){
      this.fetchInformation()
      this.$refs.editModal.show()
    },

    fetchInformation() {
      UserService.GetInformation().then(response =>{
        const data = response.data
        console.log(data)
        this.form = {
          name: data.name,
          age: data.age,
          face_image: data.face_image,
          class_name: data.class_name,
          fileList: [{
            name: "avatar.png",
            url: data.face_image,
          }],
        }
      }).catch(error =>{
        console.log(error)
      })
    },

    handlePictureCardPreview(file: UploadFile) {
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    },

    handleRemove() {
      this.$refs.uploadImage.clearFiles()
    },
    onExceed() {
      this.$message({
        message: 'Max upload one image',
        type: 'error'
      })
    },

    beforeUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isPNG = file.type === 'image/png';
      const isGIF = file.type === 'image/gif';
      const isLt5M = file.size / 1024 / 1024 < 5;

      if (!isJPG && !isPNG && !isGIF) {
        this.$message({message: 'Only jpg, png, gif files are allowed!', type: 'warning'});
        return false;
      }
      if (!isLt5M) {
        this.$message({message: 'File size cannot exceed 5MB!', type: 'warning'});
        return false;
      }
      return true;
    },

    success(data: object) {
      this.form.face_image = data.image
    },

    error() {
      this.$message({message: 'Something went wrong please try again', type: 'error'});
    },
  }
}
</script>