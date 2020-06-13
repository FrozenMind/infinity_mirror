function color(red, green, blue) {
  $.ajax({
    data: {
      red: red,
      green: green,
      blue: blue
    },
    type: 'PUT',
    url: '/color'
  }).done(data => {
    console.log('color changed')
  })
  let hexRed = red.toString(16).length == 1 ? '0' + red.toString(16) : red.toString(16)
  let hexGreen = green.toString(16).length == 1 ? '0' + green.toString(16) : green.toString(16)
  let hexBlue = blue.toString(16).length == 1 ? '0' + blue.toString(16) : blue.toString(16)
  let hex = '#' + hexRed + hexGreen + hexBlue
  document.querySelector('.color-container-outter').style.background = hex

}

function customColor() {
  let hex = document.querySelector('#color-picker').value
  let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  let r = parseInt(result[1], 16)
  let g = parseInt(result[2], 16)
  let b = parseInt(result[3], 16)
  color(r, g, b)
}

function wipe(red, green, blue) {
  $.ajax({
    data: {
      red: red,
      green: green,
      blue: blue
    },
    type: 'PUT',
    url: '/wipe'
  }).done(data => {
    console.log('color wipe started')
  })
}

function twinkleRandom() {
  $.ajax({
    data: {},
    type: 'PUT',
    url: '/twinkle-random'
  }).done(data => {
    console.log('twinkle random started')
  })
}

function runningLights() {
  $.ajax({
    data: {},
    type: 'PUT',
    url: '/running-lights'
  }).done(data => {
    console.log('running lights started')
  })
}
