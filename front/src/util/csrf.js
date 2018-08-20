export default function csrfToken() {
  const tag = document.querySelector('meta[name="authenticity_token"]');
  return tag.content;
};
