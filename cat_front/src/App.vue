 <script setup>

async function show_feed_statistics(event) {
      try
      {
           const response = await fetch('http://51.250.111.213/download_feed_stat');

           if (!response.ok) {
              throw new Error('Ошибка загрузки');
           }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.href = url;
            link.download = 'feed_stat.txt';
            link.click();

            window.URL.revokeObjectURL(url);
       }
       catch (error)
       {
            console.error('Ошибка:', error);
            alert('Не удалось скачать файл');
       }
}

async function show_pet_statistics(event)
{
      try
      {
           const response = await fetch('http://51.250.111.213/download_pet_stat');

           if (!response.ok) {
              throw new Error('Ошибка загрузки');
           }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.href = url;
            link.download = 'pet_stat.txt';
            link.click();

            window.URL.revokeObjectURL(url);
       }
       catch (error)
       {
            console.error('Ошибка:', error);
            alert('Не удалось скачать файл');
       }
}

</script>

<template>
  <header>
    <h1>
      MEPhI Networks 2025 External
    </h1>
  </header>
  <div style = "position:absolute; left: 38%; top: 9%;">
    <img src="./assets/cat.png">
  </div>

  <div style = "position:absolute; left: 39%; top: 65%; display: flex; flex-direction: column;">
    <button style = "height: 44px; width: 450px;" @click = "show_feed_statistics"> Статистика кормления кота </button>
    &nbsp;&nbsp;&nbsp;
    <button style = "height: 44px; width: 450px;" @click = "show_pet_statistics"> Попытки погладить кота </button>
  </div>

</template>

<style scoped>
header {
  position: absolute;
  top: 1%;
  left: 38%;
  font-weight: bold;
  font-size: 1.2rem;
}
</style>