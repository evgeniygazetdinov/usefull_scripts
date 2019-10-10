 var checkVideo = function() {
      if (window.matchMedia('(min-device-width: 1025px)').matches && !document.getElementById('video').src) {
        document.getElementById('video').src = document.getElementById('video').getAttribute('data-src');
      }
    }
    window.addEventListener('resize', checkVideo);
    window.addEventListener('load', checkVideo);
