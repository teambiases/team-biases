$(function() {
    $.ajax({
        url: '/titles/',
        method: 'GET',
        dataType: 'json'
    }).success(function(data) {
        $('#article-title').select2({
            data: data
        });
    });
    
    var langs, topicColors = undefined;

    $.ajax({
        url: '/langs/',
        method: 'GET',
        dataType: 'json'
    }).success(function(data) {
        langs = data;
    });
    
    $('#calculate-bias-button').click(function() {
       var k = parseInt($('#kval').val());
       var title = $('#article-title').val();
       $.ajax({
           url: '/calculate-bias/',
           method: 'GET',
           dataType: 'json',
           data: {k: k, title: title}
       }).success(function(data) {
           console.log(data);
           
           $('#article-display > div').empty();
           // Make headers for columns
           $('#target-col').append($('<h2></h2>')
                   .text(langs[0].toUpperCase() + ' ')
                   .append($('<small>target language</small>')));
           for(var i = 1; i <= 2; i++) {
               $('#spectrum-col-' + i).append($('<h2></h2>')
                       .text(langs[i].toUpperCase() + ' ')
                       .append($('<small>spectrum language</small>')));
           }
           
           if(topicColors == undefined) {
               topicColors = []
               for(var i = 0; i < data.topics.length; i++) {
                   topicColors.push(randomColor());
               }
           }
           
           data.lang = langs[0];
           data.title = title;
           displayArticle(data, 'target-col');
           for(var i = 0; i < data.similarArticles.length; i++) {
               var similarArticle = data.similarArticles[i];
               var spectrumLangId = 1;
               if(similarArticle.lang == langs[2]) { spectrumLangId = 2; }
               displayArticle(similarArticle, 'spectrum-col-' + 
                       spectrumLangId);
           }
       });
    });

    function displayArticle(article, column) {
        var articleDiv = $('<div></div>').addClass('article');
        
        // Create canvas for topics pie chart
        var topicsChartCanvas = $('<canvas></canvas>');
        articleDiv.append($('<div></div>').addClass('topics-chart-wrapper')
                .append(topicsChartCanvas));
        
        // Article title/link to Wikipedia
        var articleLink = $('<a></a>').attr('href', 'http://' + article.lang +
                '.wikipedia.org/wiki/' + article.title).text(article.readableTitle)
                .addClass('article-link');
        articleDiv.append($('<p></p>').append(articleLink));
        
        // Bias score
        if(article.hasOwnProperty('biasScore')) {
            var biasScore = $('<p></p>').addClass('bias-score')
                    .text('Bias score: ' + article.biasScore.toFixed(2));
            articleDiv.append(biasScore);
        }
        
        // Distance
        if(article.hasOwnProperty('distance')) {
            var distance = $('<p></p>').addClass('distance')
                    .text('Distance: ' + article.distance.toFixed(2));
            articleDiv.append(distance)
        }
        $('#' + column).append(articleDiv)
        
        // Draw pie chart
        var topicsLabels = [];
        for(var i = 0; i < article.topics.length; i++) {
            topicsLabels.push('Topic ' + i);
        }
        var topicsData = {
            labels: topicsLabels,
            datasets: [{
                data: article.topics,
                backgroundColor: topicColors
            }]
        };
        var topicsChartContext = topicsChartCanvas[0].getContext('2d');
        topicsChartContext.canvas.width = 300;
        topicsChartContext.canvas.height = 100;
        var topicsPieChart = new Chart(topicsChartContext, {
            type: 'pie',
            data: topicsData,
            options: {
                responsive: false,
                legend: { display: false }
            }
        });
    }
    
    function randomColor() {
        var r = Math.floor(Math.random() * 256);
        var g = Math.floor(Math.random() * 256);
        var b = Math.floor(Math.random() * 256);
        return 'rgb(' + r + ', ' + b + ', ' + g + ')'
    }

});
