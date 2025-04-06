function nextStep() {
    document.getElementById('step-1').classList.remove('active');
    document.getElementById('step-2').classList.add('active');
    document.getElementById('step1').classList.add('active');
    document.getElementById('step2').classList.add('active');
  }
  
  function prevStep() {
    document.getElementById('step-2').classList.remove('active');
    document.getElementById('step-1').classList.add('active');
    document.getElementById('step2').classList.remove('active');
  }
  