const statuses = ['Received', 'Diagnosing', 'Waiting for parts', 'Repairing', 'Ready for pickup', 'Completed', 'Cancelled'];
const starterOrders = [
  {id:'FF-1001',customerName:'Aigerim S.',phone:'+7 701 123 45 67',deviceType:'Laptop',deviceModel:'ASUS TUF Gaming A15',problem:'Laptop gets too hot and shuts down.',receivedDate:'2026-10-20',status:'Diagnosing',technician:'Arman',estimatedCost:12000,notes:'Check cooling system and clean fans.',history:[{status:'Received',date:'2026-10-20 10:20'},{status:'Diagnosing',date:'2026-10-21 09:15'}]},
  {id:'FF-1002',customerName:'Daniyar K.',phone:'+7 707 555 11 22',deviceType:'Laptop',deviceModel:'MacBook Air M1',problem:'Battery does not hold charge for long.',receivedDate:'2026-10-19',status:'Waiting for parts',technician:'Nursultan',estimatedCost:28000,notes:'Waiting for a compatible battery.',history:[{status:'Received',date:'2026-10-19 12:05'},{status:'Waiting for parts',date:'2026-10-20 11:30'}]},
  {id:'FF-1003',customerName:'Madina A.',phone:'+7 747 444 22 00',deviceType:'Phone',deviceModel:'iPhone 13',problem:'Charging port is loose.',receivedDate:'2026-10-18',status:'Ready for pickup',technician:'Arman',estimatedCost:18000,notes:'Repair completed. Customer can pick it up.',history:[{status:'Received',date:'2026-10-18 11:10'},{status:'Ready for pickup',date:'2026-10-20 17:00'}]},
  {id:'FF-1004',customerName:'Timur B.',phone:'+7 775 222 33 44',deviceType:'Laptop',deviceModel:'Lenovo IdeaPad 5',problem:'Screen flickers when moving the lid.',receivedDate:'2026-10-17',status:'Repairing',technician:'Nursultan',estimatedCost:22000,notes:'Checking the display cable.',history:[{status:'Received',date:'2026-10-17 09:40'},{status:'Repairing',date:'2026-10-18 10:00'}]},
  {id:'FF-1005',customerName:'Alina R.',phone:'+7 702 888 77 66',deviceType:'Tablet',deviceModel:'iPad 9th Gen',problem:'Glass is cracked.',receivedDate:'2026-10-15',status:'Completed',technician:'Arman',estimatedCost:35000,notes:'Picked up by the customer.',history:[{status:'Received',date:'2026-10-15 16:45'},{status:'Completed',date:'2026-10-17 13:00'}]}
];
const starterParts = [
  {id:'PT-01',name:'Laptop fan',stock:6,unitPrice:4500},
  {id:'PT-02',name:'USB-C charging port',stock:10,unitPrice:2200},
  {id:'PT-03',name:'Thermal paste',stock:14,unitPrice:1800},
  {id:'PT-04',name:'Laptop battery',stock:2,unitPrice:18000}
];
const cloneOrders = (items) => items.map((order) => ({...order,history:order.history.map((item)=>({...item}))}));
let orders = cloneOrders(starterOrders);
let parts = starterParts.map((part)=>({...part}));
const timeStamp = () => new Date().toISOString().slice(0,16).replace('T',' ');

export async function listOrders() { return cloneOrders(orders); }
export async function listParts() { return parts.map((part)=>({...part})); }
export async function createOrder(input) {
  if (!input.customerName.trim() || !input.deviceModel.trim() || !input.problem.trim()) throw new Error('Please fill in the required fields.');
  if (input.estimatedCost !== null && (!Number.isFinite(input.estimatedCost) || input.estimatedCost < 0)) throw new Error('Estimated cost must be a non-negative number.');
  if (!statuses.includes(input.status)) throw new Error('Invalid repair status.');
  const nextId = Math.max(1000, ...orders.map((order)=>Number(order.id.slice(3)) || 1000)) + 1;
  const order = {...input,id:'FF-'+nextId,history:[{status:input.status,date:timeStamp()}]};
  orders = [order,...orders];
  return cloneOrders([order])[0];
}
export async function updateOrder(id, input) {
  if (!input.customerName.trim() || !input.deviceModel.trim() || !input.problem.trim()) throw new Error('Please fill in the required fields.');
  if (input.estimatedCost !== null && (!Number.isFinite(input.estimatedCost) || input.estimatedCost < 0)) throw new Error('Estimated cost must be a non-negative number.');
  if (!statuses.includes(input.status)) throw new Error('Invalid repair status.');
  const order = orders.find((item) => item.id === id);
  if (!order) throw new Error('Repair order not found.');
  const statusChanged = order.status !== input.status;
  Object.assign(order, input);
  if (statusChanged) order.history.push({status:input.status,date:timeStamp()});
  return cloneOrders([order])[0];
}
export async function updateOrderStatus(id, status) {
  if (!statuses.includes(status)) throw new Error('Invalid repair status.');
  const order = orders.find((item)=>item.id === id);
  if (!order) throw new Error('Repair order not found.');
  order.status = status;
  order.history.push({status:status,date:timeStamp()});
  return cloneOrders([order])[0];
}
export async function savePart(id, input) {
  if (!input.name.trim()) throw new Error('Part name is required.');
  if (!Number.isFinite(input.stock) || input.stock < 0 || !Number.isFinite(input.unitPrice) || input.unitPrice < 0) throw new Error('Stock and price must be non-negative numbers.');
  if (id) {
    const part = parts.find((item)=>item.id === id);
    if (!part) throw new Error('Spare part not found.');
    Object.assign(part,input);
    return {...part};
  }
  const nextId = Math.max(0,...parts.map((part)=>Number(part.id.slice(3))||0))+1;
  const part = {id:'PT-'+String(nextId).padStart(2,'0'),...input};
  parts.push(part);
  return {...part};
}
export function resetMockData() {
  orders = cloneOrders(starterOrders);
  parts = starterParts.map((part)=>({...part}));
}
export async function getPublicOrderStatus(id) {
  const order = (await listOrders()).find((item) => item.id.toLowerCase() === id.toLowerCase());
  if (!order) return null;
  return {
    id: order.id,
    deviceModel: order.deviceModel,
    receivedDate: order.receivedDate,
    status: order.status,
    message: ({
      "Received": "Your device has been received and is waiting for a technician.",
      "Diagnosing": "A technician is checking your device to find the problem.",
      "Waiting for parts": "The repair is waiting for the required part to arrive.",
      "Repairing": "The repair is in progress.",
      "Ready for pickup": "Your device is ready. Please contact the shop to arrange pickup.",
      "Completed": "This repair has been completed.",
      "Cancelled": "This repair order has been cancelled."
    })[order.status] || "Please contact the shop for an update."
  };
}
