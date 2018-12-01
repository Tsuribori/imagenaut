import { Component } from 'react';

export default class Thread extends Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: [],
    };
  }
  componentDidMount() {
    this.getPosts();
  }
  onReplyClick = (e) => {
    const replyBox = document.getElementById('reply_box');
    e.target.parentNode.insertBefore(replyBox, e.target.parentNode.lastSibling);
    document.getElementById('id_post').value += `@${e.target.dataset.postNumber}\n`;
    window.scrollTo(0, replyBox.offsetTop);
  }
  getPosts() {
    const postLinkRe = /(@\d*)\S/g;
    document.querySelectorAll('.post_container').forEach((post) => {
     post.innerHTML = post.innerHTML.replace(postLinkRe, (e) => `<a href=#${e.replace('@', '')}>${e}</a>`); 
    });
    const postList = document.querySelectorAll("[data-type='post']");
    document.querySelectorAll('.post_number').forEach(post => post.addEventListener('click', this.onReplyClick));
    this.setState({ posts: postList });
  }
  render() {
    return null;
  }
}
