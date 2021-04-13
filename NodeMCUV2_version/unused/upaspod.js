a = Math.floor(Math.random()*100);
console.log(a)
fetch('http://localhost:5555/uppod', {
    method: 'PUT',
    body: JSON.stringify({
      "height": a
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
      'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI3YTJiNDYzZC1iNDUwLTQzMmUtYTY5Yy0xYTE0ZWZhN2Q0MjgiLCJleHAiOjE2MTgzMjU3OTR9._3Puq2NhGoYbb7JTUn_VecYkR5fsrwDorDQ3Nv2hSM8'
    ,},
  })
    .then((response) => response.json())
    .then((json) => console.log(json));