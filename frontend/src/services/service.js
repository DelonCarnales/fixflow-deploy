const useMockData = new URLSearchParams(window.location.search).get("mock") === "1";
const service = useMockData
  ? await import("./mockService.js")
  : await import("./apiService.js");

export const listOrders = (...args) => service.listOrders(...args);
export const listParts = (...args) => service.listParts(...args);
export const createOrder = (...args) => service.createOrder(...args);
export const updateOrder = (...args) => service.updateOrder(...args);
export const updateOrderStatus = (...args) => service.updateOrderStatus(...args);
export const savePart = (...args) => service.savePart(...args);
export const getPublicOrderStatus = (...args) => service.getPublicOrderStatus(...args);
