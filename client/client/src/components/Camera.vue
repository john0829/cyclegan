<template>
  <div id="camera" >
    <div class="row mb-4 justify-content-center">
      <video @click="OpenCamera()" id="video" ref="video" width="640" height="480" class="col-5" autoplay="" >
      </video>
      <img class="col-5" width="640" height="480" :src="modifiedImage">
    </div>
    <button class="btn btn-info col-1" @click="clickChangeButton()">轉換風格</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Camera',

  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      cameraIndex: 0,
      debug: '',
      modifiedImage:"./static/sampleChangeAnime.jpg",
      intervalId: 0
    }
  },

  mounted(){
    this.OpenCamera()
  },

  methods: {
    
    async OpenCamera(){
      // IPhone 無法使用 , HTC10 前鏡頭無法打開 , LG G6 可正常使用
      let video = this.$refs.video
      navigator.mediaDevices.enumerateDevices().then( (devices) => {
          devices = devices.filter( (devices) => { return devices.kind === 'videoinput'; });
          if (devices.length == 1) { // 只有一個鏡頭
            this.cameraIndex = 0
          }
          else if (this.cameraIndex == 0) { //有兩鏡頭且現在再第1鏡頭 
            this.cameraIndex = 1
          }
          else if (this.cameraIndex == 1) { //有兩鏡頭且現在再第2鏡頭
            this.cameraIndex = 0
          }
          navigator.mediaDevices.getUserMedia({ video: { deviceId: {'exact':devices[this.cameraIndex].deviceId}, facingMode: "user"  }}).then( (stream) => {
            video.src = window.URL.createObjectURL(stream);
            video.play();
          })
      })
    },
    
    getVideoImage(){
      const video = document.getElementById('video')
      const canvas = document.createElement('canvas')
      const context = canvas.getContext('2d');
      const width = video.width
      const height = video.height
      canvas.width = width
      canvas.height = height
      context.drawImage(video,0,0,width,height,0,0,width,height)
      return canvas.toDataURL("image/png").substr(22);
    },

    clickChangeButton(){
      this.upload()
    },

    upload () {
      console.log(123)
      const URL = 'http://localhost:3000/realTime'; 
      let data = new FormData();
      data.append('name', 'my-picture');
      data.append('file', this.getVideoImage()); 

      let config = {
        header : {
          'Content-Type' : 'image/png'
        }
      }

      axios.put(
        URL, 
        data,
        config
      ).then( response => {
          var Image = response['data']
          Image = Image.split("'")[1]
          this.modifiedImage = "data:image/jpeg;base64," + Image
        }
      )
    }
  }
}
</script>

<style>
#camera {
  text-align: center;
  padding: 0;
  max-width: 100%;
}

#upload {
  text-align: center;
}

</style>
