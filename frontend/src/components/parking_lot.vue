<template>
    <!-- <div v-if="openform === true">
        <subjectform @formhandler="handleformevent"></subjectform>
    </div> -->
    <div v-if="message" class="alert alert-primary" role="alert">
        {{ message }}
    </div>

    <div class="card ms-5 me-5 mt-5 shadow-lg">
        <div class="card-header d-flex">
            <h3>Parking Lots</h3>

            <router-link v-if="role==='admin'" to="admin/dashboard/create/parking_lot" class="btn btn-primary ms-auto"><i class="bi bi-patch-plus"></i>
                    Create</router-link>
        </div>
        <div class="card-body">
            <div class="row">

                <div class="col-3 " v-for="lot in lots" :key="lot.id">
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">{{ lot.name }}</h5>
                            <div>
                                <button v-if="role==='admin'" class="btn  btn-primary" @click="editlot(lot)"><i class="bi bi-pen"></i></button>
                                <button v-if="role==='admin'" class="btn btn-primary ms-2 " @click="dellot(lot.id)"><i class="bi bi-trash"></i></button> 
                                <router-link :to="`parking_lot/${lot.name}`" class="btn btn-primary ms-2">Go to parking_lot</router-link>
                            </div>
                        </div>
                    </div>
                </div>



            </div>

        </div>
    </div>

</template>
<script>

export default ({
    name: "ParkingLot",
    data() {
        return {
            lots: [],
            openform: false,
            message: "",
            greetmessage : "Hello",
            role:''

        }
    },
    methods: {
        async dellot(id){
            const token = localStorage.getItem("token")
            try{
                const response = await fetch(`http://127.0.0.1:5000/api/parking_lots?id=${id}`, {
                    method: "DELETE",
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': token
                    },

                },)
                const data = await response.json()
                if(response.status==200){
                    this.message=data.message
                    this.fetchlot()
                }
                else{
                    new Error()
                }


            }
            catch(e){
                this.message="something went worng, try again"
            }
        },

        editlot(lot){
            localStorage.setItem("parking_lot" , JSON.stringify(lot))
            this.$router.push({path:`admin/parking_lots/${lot.id}/edit`  })

        },

        
        async fetchlot() {
            const token = localStorage.getItem("token")
            const response = await fetch("http://127.0.0.1:5000/api/parking_lots", {
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': token
                }
            },)
            const data = await response.json()
            if (response.status === 200) {
                this.lots = data
            }
            else if (response.status === 401) {
                this.$router.push('/login')
            }

        }
    },
    async mounted() {
        this.role = localStorage.getItem("role")
        this.fetchlot()
    },
    
})

</script>