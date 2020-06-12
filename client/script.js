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
    console.log('color changed');
  })
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
    console.log('color wipe started');
  })
}

function twinkleRandom() {
  $.ajax({
    data: {},
    type: 'PUT',
    url: '/twinkle-random'
  }).done(data => {
    console.log('twinkle random started');
  })
}

runningLights() {
  $.ajax({
    data: {},
    type: 'PUT',
    url: '/running-lights'
  }).done(data => {
    console.log('running lights started');
  })
}
