//// src/components/PostCard.jsx
import * as React from 'react';
import Card from '@mui/material/Card';
import Avatar from '@mui/material/Avatar';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';

import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import RepeatIcon from '@mui/icons-material/Repeat';
import PersonAddIcon from '@mui/icons-material/PersonAdd';

export function PostCard({ post, onLike, onShare, onFollow }) {
  return (
    <Card variant="outlined" sx={{ maxWidth: 600, mx: 'auto', my: 2 }}>
      <CardHeader
        avatar={
          <Avatar src={`/avatars/${post.brand_name}.png`}>
            {post.brand_name[0]}
          </Avatar>
        }
        title={post.brand_name}
        subheader={new Date(post.timestamp).toLocaleString()}
      />
      <CardContent>
        <Typography variant="subtitle2" color="textSecondary" gutterBottom>
          USP: {post.usp}
        </Typography>
        <Typography variant="body1" gutterBottom>
          {post.caption}
        </Typography>
      </CardContent>

      <CardActions disableSpacing>
        <IconButton onClick={() => onLike(post.id)}>
          <FavoriteBorderIcon />
          <Typography variant="caption" sx={{ ml: 0.5 }}>
            {post.stats?.likes ?? 0}
          </Typography>
        </IconButton>

        <IconButton onClick={() => onShare(post.id)}>
          <RepeatIcon />
          <Typography variant="caption" sx={{ ml: 0.5 }}>
            {post.stats?.shares ?? 0}
          </Typography>
        </IconButton>

        <IconButton onClick={() => onFollow(post.brand_name)}>
          <PersonAddIcon />
          <Typography variant="caption" sx={{ ml: 0.5 }}>
            {post.isFollowing ? 'Following' : 'Follow'}
          </Typography>
        </IconButton>
      </CardActions>
    </Card>
  );
}