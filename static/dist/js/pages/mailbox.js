/*
 * Author: Abdullah A Almsaeed
 * Date: 4 Jan 2014
 * Description:
 *      This is a demo file used only for the main dashboard (student.html)
 **/

/* global moment:false, Chart:false, Sparkline:false */

 $(function () {
    //Enable check and uncheck all functionality
    $('.checkbox-toggle').click(function () {
      var clicks = $(this).data('clicks')
      if (clicks) {
        //Uncheck all checkboxes
        $('.mailbox-messages input[type=\'checkbox\']').prop('checked', false)
        $('.checkbox-toggle .far.fa-check-square').removeClass('fa-check-square').addClass('fa-square')
      } else {
        //Check all checkboxes
        $('.mailbox-messages input[type=\'checkbox\']').prop('checked', true)
        $('.checkbox-toggle .far.fa-square').removeClass('fa-square').addClass('fa-check-square')
      }
      $(this).data('clicks', !clicks)
    })

    //Handle starring for font awesome
    $('.mailbox-star').click(function (e) {
      e.preventDefault()
      //detect type
      var $this = $(this).find('a > i')
      var fa    = $this.hasClass('fa')

      //Switch states
      if (fa) {
        $this.toggleClass('fa-star')
        $this.toggleClass('fa-star-o')
      }
    })
  });

  function show(){
      $('#my-alert').modal('show');
  }

 function update_user(){
      var phone = document.getElementById('phone').value;
      if(!phone){
            alert('输入手机号不能为空')
        }
      else{
          $.ajax({
          url: '/update_user/',
          data: {"phone":phone},
          dataType:'json',
          success:function (data) {
              if (data === 1) {
                        alert('已更新');
                    }
                    else {
                        alert('未授权');
                    }
                },
            error: function (data) {
                 alert('Sorry，服务器可能开小差啦, 请重试!');
             }

        });
      }
}

function query_stock(){
        var station = document.getElementById('station').value;
        var sku = document.getElementById('sku').value;
        if(!station||!sku){
            alert('快取站或sku不能为空')
        }
        else {
            $.ajax({
           url: '/get_goods_count/',
           data:{"station_sn":station,"sku_id":sku},
           dataType:'json',
          success:function (data) {
               if(data){
                   alert('当日库存为'+data)
               }
            },
            error: function () {
                alert('无此key');
            }
        });
        }
  }

function update_stock(){
        var station = document.getElementById('station_sn').value;
        var sku = document.getElementById('sku_id').value;
        var goods_count = document.getElementById('goods_count').value;
        if(!station||!sku||!goods_count){
            alert('快取站和sku不能为空或数量不能为空')
        }
        else {
            $.ajax({
           url: '/set_goods_count/',
           data:{"station_sn":station,"sku_id":sku,"goods_count":goods_count},
           dataType:'json',
          success:function (data) {
               alert('库存为'+data)
            },
            error: function () {
                alert('Sorry，服务器可能开小差啦, 请重试!');
            }
        });
        }
  }

  function update_link() {
      var my_link = document.getElementById('my_link').value;

      if(!my_link){
            alert('输入短链不能为空')
        }

      else {
          console.info(my_link);
          $.ajax({
              type:'post',
              data:{"my_link":my_link},
              url: '/update_link/',
        success:function (data) {
            alert(data);
        },
        error: function () {
            alert('转换失败');
        }

        });
      }

  }

  function query_count() {
       $.ajax({
          url: '/get_limit_count/',
          success:function (data) {
               alert('当前限制购买份数为'+data)
            },
            error: function () {
                alert('Sorry，服务器可能开小差啦, 请重试!');
            }

        });
  }
   function set_count() {
        var count = document.getElementById('count').value;
        if(!count){
            alert('输入数量不能为空')
        }
        else {
             $.ajax({
           url: '/set_limit_count/',
           data:{'count':count},
           dataType:'json',
           success: function (data) {
               alert('当前限制购买份数为'+data)
           },
           error: function () {
               alert('Sorry，服务器可能开小差啦, 请重试!');
           }

       });
        }

   }