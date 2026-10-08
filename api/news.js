export default async function handler(req, res) {
  const API_KEY = "d3faacc7d17546cf8ddce6b3d7264343";
  const { category, q } = req.query;

  let url = "";
  if (q) {
    url = `https://newsapi.org/v2/everything?q=${encodeURIComponent(q)}&sortBy=publishedAt&language=en&pageSize=25&apiKey=${API_KEY}`;
  } else {
    const catParam = (category && category !== "all") ? `&category=${category}` : "";
    url = `https://newsapi.org/v2/top-headlines?language=en&pageSize=25${catParam}&apiKey=${API_KEY}`;
  }

  try {
    const response = await fetch(url, {
      headers: {
        "User-Agent": "WorldNewsApp/1.0"
      }
    });
    const data = await response.json();
    return res.status(200).json(data);
  } catch (err) {
    return res.status(500).json({ status: "error", message: err.message });
  }
}
