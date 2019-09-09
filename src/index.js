const AWS = require('aws-sdk/global')
const S3 = require('aws-sdk/clients/s3')

let width = 320  // will be scaled to this width
let height = 0

let streaming = false

const video = document.getElementById('video')
const freshBtn = document.getElementById('fresh')
const rottenBtn = document.getElementById('rotten')

AWS.config.region = 'ap-southeast-1'
AWS.config.credentials = new AWS.Credentials({
  accessKeyId: process.env.ACCESS_KEY,
  secretAccessKey: process.env.SECRET_KEY
})
const s3 = new S3()

navigator.mediaDevices.getUserMedia({ video: true, audio: false })
  .then(stream => {
    video.srcObject = stream
    video.play()
  })
  .catch(console.error)

video.addEventListener('canplay', ev => {
  if (!streaming) {
    height = video.videoHeight / (video.videoWidth/width)

    video.setAttribute('width', width)
    video.setAttribute('height', height)
    streaming = true
  }
}, false)

freshBtn.addEventListener('click', ev => {
  takepicture('fresh')
  ev.preventDefault()
}, false)

rottenBtn.addEventListener('click', ev => {
  takepicture('rotten')
  ev.preventDefault()
}, false)

function takepicture(type) {
  const canvas = document.createElement('canvas')
  if (width && height) {
    canvas.width = width
    canvas.height = height
    const context = canvas.getContext('2d')

    canvas.toBlob(blob => {
      const epoch = new Date().getTime()
      const params = {
        Bucket: 'aws-freshgrade',
        Key: `${type}/${epoch}.webp`,
        Body: blob
      }
      s3.upload(params, (err, data) => {
        if (err) {
          console.error('s3 error', err)
        } else {
          console.info('uploaded', data)
        }
      })
    }, 'image/webp')
  }
}
