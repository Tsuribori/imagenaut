import { Component } from 'react';

const axios = require('axios');

export default class Thread extends Component {
  componentDidMount() {
    this.getPosts();
  }

  componentWillUnmount() {
    document.querySelectorAll('.post_number').forEach(post => post.removeEventListener('click', this.onReplyClick));
    document.querySelectorAll('.image').forEach(image => image.removeEventListener('click', this.onImageClick));
    const postUnlinkRe = /(<a class=postlink href=(?:.*)>@\d*<\/a>)/g;
    document.querySelectorAll('.post_container').forEach((post) => {
      post.innerHTML = post.innerHTML.replace(postUnlinkRe, e => e);
    });
    document.querySelectorAll('.post_link').forEach((link) => {
      link.removeEventListener('mouseover', this.onLinkHover);
      link.removeEventListener('mouseleave', this.onLinkLeave);
    });
  }

  onReplyClick = (e) => {
    const replyBox = document.getElementById('reply_box');
    e.target.parentNode.insertBefore(replyBox, e.target.parentNode.lastSibling);
    document.getElementById('id_post').value += `@${e.target.dataset.postNumber}\n`;
    window.scrollTo(0, replyBox.offsetTop);
  }

  onImageClick = (e) => {
    e.preventDefault();
    const image = e.target;
    if (image.getAttribute('data-expanded') !== '1') {
      image.setAttribute('src', image.parentNode.getAttribute('href'));
      image.setAttribute('data-other-height', image.getAttribute('height'));
      image.setAttribute('height', 'auto');
      image.setAttribute('data-other-width', image.getAttribute('width'));
      image.setAttribute('width', 'auto');
      image.setAttribute('data-expanded', '1');
    } else {
      image.setAttribute('src', image.getAttribute('data-url'));
      image.setAttribute('height', image.getAttribute('data-other-height'));
      image.setAttribute('width', image.getAttribute('data-other-width'));
      image.setAttribute('data-expanded', '0');
    }
  }

  onLinkHover = (e) => {
    const linkTarget = e.target.getAttribute('href').replace('#', '');
    axios.get(`/board/ajax/${linkTarget}`).then((response) => {
      if (response.status === 200) {
        const parser = new DOMParser();
        const fetchedDocument = parser.parseFromString(response.data, 'text/html');
        const fetchedPost = fetchedDocument.getElementById(linkTarget);
        fetchedPost.style.position = 'absolute';
        fetchedPost.style.left = e.pageX;
        fetchedPost.style.top = e.pageY;
        fetchedPost.setAttribute('data-hovered', '1');
        document.getElementById('thread_container').appendChild(fetchedPost);
      }
    }).catch(() => {
      e.target.style.cursor = 'not-allowed';
    });
  }

  onLinkLeave = () => {
    const hovered = document.querySelectorAll('[data-hovered]');
    hovered.forEach(post => post.remove());
  }

  getPosts() {
    const postLinkRe = /(@\d*)\b/g;
    /* eslint no-param-reassign: "off" */
    document.querySelectorAll('.post_container').forEach((post) => {
      post.innerHTML = post.innerHTML.replace(postLinkRe, e => `<a class=post_link href=#${e.replace('@', '')}>${e}</a>`);
    });
    /* eslint no-param-reassign: "error" */
    document.querySelectorAll('.post_link').forEach((link) => {
      link.addEventListener('mouseover', this.onLinkHover);
      link.addEventListener('mouseleave', this.onLinkLeave);
    });
    document.querySelectorAll('.post_number').forEach((post) => {
      post.addEventListener('click', this.onReplyClick);
      post.style.cursor = 'pointer';
    });
    document.querySelectorAll('.image').forEach(image => image.addEventListener('click', this.onImageClick));
  }

  render() {
    return null;
  }
}
