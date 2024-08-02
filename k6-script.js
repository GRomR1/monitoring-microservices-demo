import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '20s',
};

export default function () {
  const res = http.get('http://localhost:8001/users');
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(0.5);
}