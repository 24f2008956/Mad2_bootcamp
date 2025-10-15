<template>
    <div v-if="message" class="alert alert-primary" role="alert">
        {{ message }}
    </div>

    <div class="card ms-auto me-auto mt-3" style="width:50%">
        <div class="card-body">
    <!-- Parking Lot Name -->
    <div class="form-floating mb-3">
        <input type="text" v-model="formdata.name" class="form-control" id="parkingLotName">
        <label for="parkingLotName">Parking Lot Name</label>
    </div>

    <!-- Address -->
    <div class="form-floating mb-3">
        <input type="text" v-model="formdata.address" class="form-control" id="parkingLotAddress">
        <label for="parkingLotAddress">Address</label>
    </div>

    <!-- Pincode -->
    <div class="form-floating mb-3">
        <input type="text" v-model="formdata.pincode" class="form-control" id="parkingLotPincode">
        <label for="parkingLotPincode">Pincode</label>
    </div>

    <!-- Price Per Hour -->
    <div class="form-floating mb-3">
        <input type="number" step="0.01" v-model="formdata.price_per_hour" class="form-control" id="parkingLotPrice">
        <label for="parkingLotPrice">Price per Hour</label>
    </div>

    <!-- Max Number of Spots -->
    <div class="form-floating mb-3">
        <input type="number" v-model="formdata.max_no_spots" class="form-control" id="parkingLotSpots">
        <label for="parkingLotSpots">Maximum Number of Spots</label>
    </div>
</div>  

            <button class="btn btn-primary mt-3" @click="iseditMode ? edit() : submit()">{{ iseditMode ? 'Edit' : 'Create'
                }}</button>

        </div>
    </div>

</template>
<script>
export default ({
    name: "LoginComp",
    data() {
        return {
            formdata: {
                name: '',
                address: '',
                pincode: '',
                price_per_hour: null,
                max_no_spots: null
            },
            message: "",
            iseditMode: false
        }
    },
    methods: {
        async submit() {
            console.log(this.formdata)
            const token = localStorage.getItem("token")
            try {
                const response = await fetch("http://127.0.0.1:5000/api/Parking_lots", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': token
                    },
                    body: JSON.stringify(this.formdata)

                },)
                const data = await response.json()
                console.log(data)

                if (response.status === 200) {

                    this.$router.push("/admin/dashboard")

                }
                else if (response.status == 409) {

                    this.message = data.message
                }
                else if (response.status == 500) {

                    this.message = "Something went wrong, Try again"
                }
            }
            catch (e) {
                this.message = e.message
            }


        },
        async edit() {
            console.log(this.formdata)
            const token = localStorage.getItem("token")
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/Parking_lots?id=${this.formdata.id}`, {
                    method: "PUT",
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': token
                    },
                    body: JSON.stringify(this.formdata)

                },)
                const data = await response.json()
                console.log(data)

                if (response.status === 200) {
                    localStorage.removeItem("lot")

                    this.$router.push("/admin/dashboard")

                }
                else if (response.status == 409) {

                    this.message = data.message
                }
                else if (response.status == 404) {

                    this.$router.push("/admin/dashboard")
                }
            }
            catch (e) {
                this.message = e.message
            }

        }

    },
    mounted() {
        this.formdata = { ...JSON.parse(localStorage.getItem("parking_lot")) }
        if (this.formdata.name) {
            this.iseditMode = true
        }
        console.log(this.formdata)



    },
    unmounted(){
        localStorage.removeItem("parking_lot")
    }

})

</script>