
// 1번 과제
// "주문하기" 버튼 클릭시 아래 함수 호출을 위해 HTML 태그에 onClick을 선언해줍니다. 
function submitOrder() {
    /* 
      입력값에 대한 체크 작업을 "유효성 검사 (Input validation)" 이라 합니다. (ex: 빈칸 여부, 전화번호 포맷 체크)
      input이 있다면 반드시 따라오는 작업입니다! 꼭 기억해두세요! 
      추후 구글링시 빈번하게 활용될 수 있는 키워드이므로 기억해두세요! (구글링 해보기)
    */

    // 변수 : 변경될 수 있는 값을 담기 위해 필요합니다. (ex: 주문자 이름, 수량, 주소, 전화번호)
    // $().val() : 특정 input 태그의 값 가져오기 (위 $().val('A')와 비교)
    let name = $('#input-name').val();
    let count = $('#input-count').val();
    let address = $('#input-address').val();
    let phone = $('#input-phone').val();

    // 조건문 : 상황/경우에 따라 다른 기능을 수행하기 위해 사용합니다. (ex: 값 입력 안된 경우 or 입력 모두 된 경우)
    if (name === '') {
      alert('주문자 이름을 입력해주세요.')
      // $().focus() : 특정 input 태그에 포커스가 맞춰지도록 하기
      $('#input-name').focus()
    } else if (count === '') {
      // 위 조건문을 위해 HTML 태그에서 디폴트 옵션 부분에 value=''를 선언해줘야 합니다. 
      alert('수량을 입력해주세요.')
      $('#input-count').focus()
    } else if (address === '') {
      alert('주소를 입력해주세요.')
      $('#input-address').focus()
    } else if (phone === '') {
      alert('전화번호를 입력해주세요.')
      $('#input-phone').focus()
    } else if (!isValidPhoneNum(phone)) {
      // 함수 : 여러번 사용될 만한 기능을 묶어두기 위해 사용합니다. (ex: 전화번호 포맷 유효성 검사)
      alert('휴대폰번호 입력 형식이 틀립니다.\n010-0000-0000으로 입력해주세요.')
    } else {
      alert("주문완료!")
      // $().val('A') : 특정 input 태그에 값 입력하기 
      $('#input-name').val('');
      $('#input-count').val('');
      $('#input-address').val('');
      $('#input-phone').val('');
    }
}

function isValidPhoneNum(phone) {
    // 조건 : A-B-C (A : 010,  B : 숫자 4자리, C:  숫자 4자리)
    // 방법?
    // 1) '-'로 split 한다. 이때 무조건 3조각으로 나뉘어야 한다.
    // 2) A조각은 무조건 010
    // 3) B와 C조각은 숫자로 이루어진 4자리 
    let splitByHyphen = phone.split('-')
    if (splitByHyphen.length != 3) {
        return false;
    } else if (splitByHyphen[0] !== '010') {
        return false;
    } else if (isNaN(splitByHyphen[1]) || isNaN(splitByHyphen[2])) {
        // google : js check string is number
        // https://stackoverflow.com/questions/175739/built-in-way-in-javascript-to-check-if-a-string-is-a-valid-number
        return false;
    } else if (splitByHyphen[1].length !== 4 || splitByHyphen[2].length !== 4) {
        return false;
    }
    return true;
}


// Advnaced : 찜 목록 기능을 넣고 싶다면? 
function addWishlist() {
    let heart = $("#button-wish").text();
    if (heart == '♥') {
        alert('찜이 취소되었습니다.')
        $("#button-wish").text('♡')
    } else {
        $('#wishModal').modal('toggle')
        $("#button-wish").text('♥')
    }
}

// Advanced : 다른 페이지로 이동시키기
function moveToWishList() {
    window.open("http://naver.com")
    $('#wishModal').modal('hide')
}
// 하지만 새로고침을 한다면? 다시 돌아옵니다. 유지시키려면 -> 백엔드 개발과 DB 필요!


// 2번 과제
// 화면 로드가 완료된 후 함수를 실행시키려는 경우 아래 코드를 사용합니다. (단축어 : jqDocReady )
// 새로운 것이긴 하지만 사실 onClick과 아래 코드면 거의 대부분을 다룰 수 있습니다. (2개만 기억하기!)
$(document).ready(function(){
	getExchangeRateInfo()
})

function getExchangeRateInfo(){
  $.ajax({
    type: "GET",
    url: "https://api.manana.kr/exchange/rate.json",
    data: {},
    success: function (response) {
      // 우선 console.log(response) 를 통해 API 결과의 구조를 파악하고 진행합니다. 
      let exchangeRateInfo = response[1]['rate']
      // input이 아닌 다른 태그에 대해 내부 값을 넣는 방법
      $("#exchange-rate-info").text(exchangeRateInfo);
    }
  })
}