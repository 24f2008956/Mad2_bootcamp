<template>
  <div class="container mt-5">
    <div class="card shadow-lg">
      <div class="card-header d-flex align-items-center">
        <h3>Edit Parking Lot</h3>
        <router-link to="/admin/dashboard" class="btn btn-secondary ms-auto">
          <i class="bi bi-arrow-left"></i> Back
        </router-link>
      </div>

      <div class="card-body">
        <div v-if="message" :class="['alert', success ? 'alert-success' : 'alert-danger']">
          {{ message }}
        </div>

        <form @submit.prevent="updateLot">
          <div class="mb-3">
            <label class="form-label">Name</label>
            <input v-model="lot.name" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Address</label>
            <input v-model="lot.address" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Pincode</label>
            <input v-model="lot.pincode" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Price per Hour</label>
            <input v-model.number="lot.price_per_hour" type="number" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Max No. of Spots</label>
            <input v-model.number="lot.max_no_spots" type="number" class="form-control" required />
          </div>

          <button class="btn btn-primary" type="submit">
            <i class="bi bi-save"></i> Update Lot
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "edit_lot",
  data() {
    return {
      lot: {
        name: "",
        address: "",
        pincode: "",
        price_per_hour: 0,
        max_no_spots: 0
      },
      message: "",
      success: false
    };
  },
  async mounted() {
    const id = this.$route.params.id;
    await this.fetchLotDetails(id);
  },
  methods: {
    async fetchLotDetails(id) {
      const token = localStorage.getItem("token");
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/parking_lots?${id}`, {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": token
          }
        });
        if (res.status === 200) {
          this.lot = await res.json();
        } else if (res.status === 401) {
          this.$router.push("/login");
        } else {
          this.message = "Failed to fetch parking lot details";
          this.success = false;
        }
      } catch (e) {
        this.message = "Error loading lot data";
        this.success = false;
      }
    },

    async updateLot() {
      const token = localStorage.getItem("token");
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/parking_lots/${this.$route.params.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": token
          },
          body: JSON.stringify(this.lot)
        });
        const data = await res.json();
        if (res.status === 200) {
          this.message = data.message;
          this.success = true;
          setTimeout(() => this.$router.push("/admin/dashboard"), 1500);
        } else {
          this.message = data.message || "Update failed";
          this.success = false;
        }
      } catch (e) {
        this.message = "Something went wrong during update";
        this.success = false;
      }
    }
  }
};
</script>

<style scoped>
.card {
  max-width: 600px;
  margin: auto;
  border-radius: 1rem;
}
</style>
