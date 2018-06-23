<template>
  <div class="hello container">
    <div class="row justify-content-center">
      <img class="preview col-3" :src="imageData">
      <div class="col-2"></div>
      <img class="col-3" :src="modifiedImage">
    </div>
    <div class="row justify-content-center">
      <div class="file-upload-form col-4">
        <input type="file" @change="previewImage" accept="image/*">
      </div>
      <div class="col-2"></div>
        <button class="btn btn-success col-2" @click="uploadImage()">改變成真人風格</button>
        <button class="btn btn-success col-1" id="downloadButton" @click="downloadImage()">下載</button>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      imageData:"./static/sampleAnime.jpg",
      modifiedImage:"./static/sampleChangeReal.jpg"
    }
  },
  methods:{
    previewImage (event) {
      const input = event.target;
      if (input.files && input.files[0]) {
          const reader = new FileReader();
          reader.onload = (e) => {
              this.imageData = e.target.result;
          }
          reader.readAsDataURL(input.files[0]);
    }
    },
    uploadImage(){
      const URL = 'http://localhost:3000/uploadToReal'; 
      let data = new FormData();
      data.append('name', 'my-picture');
      data.append('file', this.imageData); 

      let config = {
        header : {
          'Content-Type' : 'image/png'
        }
      }
      if(this.imageData.length > 100)
      {
        axios.put(
          URL, 
          data,
          config
        ).then(
          response => {
            var Image = response['data']
            Image = Image.split("'")[1]
            this.modifiedImage = "data:image/jpeg;base64," + Image
          }
        )
      }
    },
    downloadImage(){
      axios({
        url: 'http://localhost:3000/outfileReal.jpg',
        method: 'GET',
        responseType: 'blob', // important
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'outfile.jpg');
        document.body.appendChild(link);
        link.click();
      });
    }
  }

}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

img{
  width:300px;
  height:300px;
}

#downloadButton{
  margin-left: 5%;
}
</style>
