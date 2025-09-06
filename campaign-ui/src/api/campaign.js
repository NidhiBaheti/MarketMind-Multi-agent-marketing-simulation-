// src/api/campaigns.js
export async function getCampaigns() {
  const res = await fetch("http://localhost:8000/campaigns/");
  return res.ok ? res.json() : [];
}

export async function likeCampaign(id) {
  await fetch(`http://localhost:8000/campaigns/${id}/like`, { method: "POST" });
}

export async function shareCampaign(id) {
  console.log("Shared campaign", id);
}

export async function followBrand(brandName) {
  await fetch(`http://localhost:8000/brands/${brandName}/follow`, { method: "POST" });
}