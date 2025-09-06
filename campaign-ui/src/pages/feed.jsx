import React, { useState, useEffect } from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import IconButton from "@mui/material/IconButton";

import HomeIcon from "@mui/icons-material/Home";
import SearchIcon from "@mui/icons-material/Search";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

import { PostCard } from "../components/postcard";
import {
  getCampaigns,
  likeCampaign,
  shareCampaign,
  followBrand,
} from "../api/campaign";

export function Feed() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchData = () => getCampaigns().then((data) => setPosts(data.reverse()));
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <AppBar position="sticky" color="default" elevation={1}>
        <Toolbar sx={{ justifyContent: "space-between" }}>
          <Typography variant="h6">MarketMind</Typography>
          <Box>
            <IconButton><HomeIcon /></IconButton>
            <IconButton><SearchIcon /></IconButton>
            <IconButton><NotificationsNoneIcon /></IconButton>
            <IconButton><AccountCircleIcon /></IconButton>
          </Box>
        </Toolbar>
      </AppBar>

      <Box sx={{ display: "flex" }}>
        <Container maxWidth="md" sx={{ mt: 2, mb: 4 }}>
          {posts.map((post) => (
            <PostCard
              key={post.id}
              post={post}
              onLike={likeCampaign}
              onShare={shareCampaign}
              onFollow={followBrand}
            />
          ))}
        </Container>
      </Box>
    </>
  );
}