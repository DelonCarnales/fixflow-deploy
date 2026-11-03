import test from 'node:test';
import assert from 'node:assert/strict';
import {listOrders,createOrder,updateOrder,updateOrderStatus,listParts,savePart,resetMockData} from './mockService.js';

test.beforeEach(()=>resetMockData());

test('starts with sample repair orders',async()=>{const orders=await listOrders();assert.equal(orders.length,5);assert.equal(orders[0].id,'FF-1001');});
test('creates an order with a new number and history',async()=>{const order=await createOrder({customerName:'Test',phone:'',deviceType:'Laptop',deviceModel:'Test laptop',problem:'Will not start',receivedDate:'2026-10-22',status:'Received',technician:'',estimatedCost:null,notes:''});assert.equal(order.id,'FF-1006');assert.equal(order.history.length,1);});
test('records status changes',async()=>{const order=await updateOrderStatus('FF-1001','Repairing');assert.equal(order.status,'Repairing');assert.equal(order.history.at(-1).status,'Repairing');});
test('rejects negative part stock and price',async()=>{
  await assert.rejects(()=>savePart('',{name:'Test part',stock:-1,unitPrice:100}),/non-negative/);
  await assert.rejects(()=>savePart('',{name:'Test part',stock:1,unitPrice:-100}),/non-negative/);
});
test('adds a spare part with the next ID',async()=>{const part=await savePart('',{name:'HDMI cable',stock:3,unitPrice:1200});assert.equal(part.id,'PT-05');assert.equal((await listParts()).length,5);});
test('rejects an unknown repair order',async()=>{await assert.rejects(()=>updateOrderStatus('FF-9999','Repairing'),/not found/);});
test('edits an order and records a changed status',async()=>{const before=(await listOrders())[0];const updated=await updateOrder(before.id,{customerName:'Edited Customer',phone:before.phone,deviceType:before.deviceType,deviceModel:'Edited Laptop',problem:'Updated problem',receivedDate:before.receivedDate,status:'Repairing',technician:before.technician,estimatedCost:5000,notes:'Updated notes'});assert.equal(updated.customerName,'Edited Customer');assert.equal(updated.deviceModel,'Edited Laptop');assert.equal(updated.status,'Repairing');assert.equal(updated.history.at(-1).status,'Repairing');assert.equal((await listOrders())[0].notes,'Updated notes');});
test('edits a part by its ID even when its name changes',async()=>{const part=await savePart('PT-02',{name:'New charging port',stock:7,unitPrice:2500});assert.equal(part.id,'PT-02');assert.equal(part.name,'New charging port');assert.equal((await listParts()).find((item)=>item.id==='PT-02').stock,7);});
