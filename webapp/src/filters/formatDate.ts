import Vue from 'vue';

Vue.filter('formatDate', function (dateString: string) {
  const date = new Date(dateString);
  const options: any = { month: 'short', day: 'numeric' };
  if (date.getFullYear() !== new Date().getFullYear()) {
    options.year = 'numeric';
  }
  return date.toLocaleDateString(undefined, options);
});
