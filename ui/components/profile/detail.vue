<template>
  <v-container v-if="profile">
    <v-row justify="center" align="center">
      <v-col cols="8" sm="4" md="4">
        <div class="text-center"></div>
        <v-card>
          <v-card-text>
            <div>{{ profile.id }}</div>
            <div>{{ profile.議員氏名 }}</div>
            <div>{{ profile.会派 }}</div>
            <!-- <ul>
              <li v-for="item in social" :key="item.title">
                <a
                  :href="item.link"
                  target="_blank"
                  rel="noopener noreferrer"
                  >{{ item.title }}</a
                >
              </li>
            </ul> -->
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="4" sm="4" md="2">
        <v-avatar class="profile" color="grey" size="164" tile>
          <v-img
            src="https://www.sangiin.go.jp/japanese/joho1/kousei/giin/photo/g7004004.jpg"
          ></v-img>
        </v-avatar>
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-text>
            <!-- <p>
              １９５７年大分県大分市に生まれる。大分県立大分舞鶴高等学校を経て、１９８２年筑波大学医学専門学群卒業、同年５月医籍登録、１９９０年学位を授与される（医学博士・筑波大学）。
            </p>
            <p>
              １９９４年筑波大学臨床医学系外科講師、１９９６年日本外科学会指導医（専門医・認定医）、２０００年日本消化器外科学会指導医（専門医・認定医）、２００１年日本癌治療学会認定臨床試験登録医の資格を取得。
            </p>
            <p>
              ２００３年筑波大学臨床医学系外科助教授、２００４年筑波メディカルセンター病院診療部長に就任、１９９８年から２０１０年まで日本胃癌学会評議員を務める。
            </p>
            <p>
              ２００４年第２０回参議院議員選挙（大分県選出）で初当選、医療を中心とした社会保障の改革に力を注ぐ○元厚生労働大臣政務官○元民進党、国民民主党政務調査会長○現在厚生労働委員会理事、倫選特委員会理事、国民民主党組織委員長、税制調査会副会長、大分県連代表○筑波大学客員教授
            </p>
            <p>（令和元年１２月１０日現在）</p> -->
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  layout(context) {
    return "default";
  },
  props: {
    id: null,
  },
  data() {
    return {
      profile: null,
      // profile: {
      //   id: 1,
      //   議員氏名: "ｱﾝﾄﾆｵ　猪木",
      //   議員氏名読み方: "あんとにお　いのき",
      //   会派: "国民民主党・新緑風会",
      //   性別: "男",
      //   本名: "猪木　寛至",
      //   本名読み方: null,
      //   別名: null,
      //   備考: null,
      // },
    };
  },
  async fetch() {
    const url = "http://localhost:8080/person/get_profile";
    const tmp = await this.$axios
      .$get(url, {
        params: { id: this.id },
      })
      .catch((err) => {
        if (err.response.status == 404) {
          // TODO: 404時の処理をどうするか
          this.profile = null;
        } else {
          this.$accessor.notify.pushMessage(JSON.stringify(err.response));
        }
      });
    this.profile = tmp;
  },
});
</script>
