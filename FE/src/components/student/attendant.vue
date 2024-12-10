<template>
  <el-dialog v-model="rolesModal" style="width: 70%;min-width:400px;height: fit-content;" :show-close="false">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-table v-loading="loading.table" :data="attendantList" fit>
          <el-table-column
              label="No.0"
              width="80"
          >
            <template v-slot:default="scope">
              <div>
                {{ scope.$index + 1 + (query.page - 1) * query.perPage}}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Message"
          >
            <template v-slot:default="{row}">
              <div>
                {{ row.type_check ? 'You join the session' : 'You left the session' }}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Subject"
          >
            <template v-slot:default="{row}">
              <div>
                {{ row.subject && row.subject.name }}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Teacher"
          >
            <template v-slot:default="{row}">
              <div>
                {{ row.teacher && row.teacher.name }}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Session time start"
              min-width="140"
          >
            <template v-slot:default="{row}">
              <div>
                {{ `${getDayOfWeek(row.session.start_at)}, ${changeTimestampToTime(row.session.start_at/1000)}` }}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Attendant time"
          >
            <template v-slot:default="{row}">
              <div>
                {{ changeTimestampToTime(row.attendant_time) }}
              </div>
            </template>
          </el-table-column>
          <el-table-column
              label="Status"
          >
            <template v-slot:default="{row}">
              <div>
                {{ row.attendant_time > row.session.start_at/1000 ? 'You late' : '' }}
              </div>
            </template>
          </el-table-column>
        </el-table>
        <div v-if="total > 0" class="demo-pagination-block pagination">
          <el-pagination
              v-model:current-page="query.page"
              v-model:page-size="query.perPage"
              :page-sizes="[10, 20, 50, 100]"
              size="default"
              layout="sizes, prev, pager, next"
              :total="total"
              @size-change="sizeChange"
              @current-change="pageChange"
          />
        </div>
      </el-col>
    </el-row>
  </el-dialog>
</template>

<script lang="ts">
import {Edit, Delete, ZoomIn, Plus} from "@element-plus/icons-vue"
import { ROLES } from "@/utils/constant";
import GlobalModal from "@/components/common/global-modal.vue";
import AttendantService from "@/service/attendent-api/api";
import { changeTimestampToTime } from '@/utils/function'

export default {
  name: 'RolesComponent',
  data() {
    return{
      rolesModal: false,
      roles:[],
      loading: {
        roles: false,
        class: false,
        table: false,
        subject: false
      },
      attendantList: [],
      query: {
        name: '',
        role: ROLES.STUDENT,
        page: 1,
        perPage: 20,
      },
      total: 20,
      form: {
        name: '',
        age: null,
        role: 'student',
        face_image: '',
        class_id: null,
        gender_id: null,
        fileList: [],
        subject: []
      },
      genderList: [
        {
          id: 1,
          name: 'male'
        },
        {
          id: 2,
          name: 'female'
        }
      ],
      rules: {},
      classList: [],
      subjectList: [],
      classDebounce: null,
      subjectDebounce: null,
      dialogVisible: false,
      dialogImageUrl: "",
      userDeleteId: null
    }
  },
  components:{
    Plus, ZoomIn,
    GlobalModal,
    Edit, Delete
  },
  created() {
    this.fetchAttendant()
  },
  methods:{
    changeTimestampToTime,

    getDayOfWeek(timestamp) {
      const daysOfWeek = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
      ];
      const date = new Date(timestamp);
      return daysOfWeek[date.getDay()];
    },

    show(){
      //reset data
      this.query = {
        name: '',
        role: ROLES.STUDENT,
        page: 1,
        perPage: 20,
      }
      this.rolesModal = true
    },

    fetchAttendant(filter){
      AttendantService.GetAttendant(filter).then((data) => {
        this.attendantList = data.data
      }).catch(error =>{
        console.log(error)
      })
    },

    sizeChange(size: number){
      this.query.perPage = size
    },

    pageChange(page :number){
      this.query.page = page
    },

    searching(){
    },

    success(data: object){
      this.form.face_image = data.image
    },

    error(){
      this.$message({message:'Something went wrong please try again',type:'error'});
    },

    openConfirmModal(data){
      this.userDeleteId = data.id
      this.$refs.confirmModal.show()
    },

  }
}
</script>

<style scoped>

</style>