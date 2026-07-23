(function () {
  var COPY = {
    en: {
      badge: "Suggested path",
      defaultTitle: "Start here.",
      fromSource: "Coming from {source}? Start here.",
      body: "Use this guide in the order that keeps it useful: compare first, check signup requirements next, and only open the official referral link if Rakuten still looks like the best fit.",
      note: "The referral incentive is disclosed in the final section, and this guide also points out when Rakuten is not the right choice.",
      ctaEyebrow: "Official link, if Rakuten still looks like the best fit",
      ctaTitle: "If Rakuten looks right after comparing, you can apply here",
      ctaText: "This is the official employee referral link. It applies the referral program automatically, but you should only use it if Rakuten fits your area, budget, and setup needs better than the alternatives above.",
      ctaButton: "Open official referral link →",
      sources: {
        reddit: "Reddit",
        quora: "Quora",
        devto: "dev.to",
        hashnode: "Hashnode",
        threads: "Threads",
        search: "search",
        article: "an article"
      },
      steps: {
        compare: "Compare plans",
        simulator: "Use the cost calculator",
        requirements: "Check signup requirements",
        faq: "Read the FAQ",
        howto: "See the signup steps",
        apply: "Open the official link"
      }
    },
    ko: {
      badge: "추천 순서",
      defaultTitle: "여기부터 보세요.",
      fromSource: "{source}에서 오셨다면 여기부터 보세요.",
      body: "이 페이지를 가장 유용하게 보는 순서는 이렇습니다. 먼저 비교하고, 다음으로 가입 요건을 확인한 뒤, 라쿠텐이 가장 잘 맞는다고 판단될 때만 공식 소개 링크를 여세요.",
      note: "소개 인센티브는 마지막 섹션에서 공개되어 있으며, 이 가이드는 라쿠텐이 맞지 않는 경우도 함께 설명합니다.",
      ctaEyebrow: "라쿠텐이 가장 잘 맞는다고 판단될 때만 여는 공식 링크",
      ctaTitle: "비교 후 라쿠텐이 맞는 선택이라면 여기서 신청하세요",
      ctaText: "이 링크는 공식 직원 소개 링크입니다. 소개 프로그램이 자동으로 적용되지만, 위의 대안보다 라쿠텐이 지역, 예산, 개통 편의성 면에서 더 잘 맞을 때만 사용하세요.",
      ctaButton: "공식 소개 링크 열기 →",
      sources: {
        reddit: "Reddit",
        quora: "Quora",
        devto: "dev.to",
        hashnode: "Hashnode",
        threads: "Threads",
        search: "검색",
        article: "글"
      },
      steps: {
        compare: "요금제 비교 보기",
        simulator: "비용 계산기 사용",
        requirements: "가입 요건 확인",
        faq: "FAQ 읽기",
        howto: "가입 절차 보기",
        apply: "공식 링크 열기"
      }
    },
    "zh-Hans": {
      badge: "推荐阅读顺序",
      defaultTitle: "建议从这里开始。",
      fromSource: "如果你是从{source}点进来的，建议先看这里。",
      body: "为了让这页真正有用，建议按这个顺序看：先比较，再确认签约条件，只有当你觉得Rakuten确实最适合时，再打开官方员工推荐链接。",
      note: "员工推荐激励已在最后部分明确披露，本指南也会直接说明哪些情况下Rakuten并不是最佳选择。",
      ctaEyebrow: "只有当Rakuten仍然最适合你时，再打开这个官方链接",
      ctaTitle: "如果比较之后你仍然认为Rakuten最合适，可以在这里申请",
      ctaText: "这是官方员工推荐链接，会自动套用推荐计划。但只有在Rakuten比上面的其他选择更适合你的地区、预算和开通需求时，才建议使用。",
      ctaButton: "打开官方推荐链接 →",
      sources: {
        reddit: "Reddit",
        quora: "Quora",
        devto: "dev.to",
        hashnode: "Hashnode",
        threads: "Threads",
        search: "搜索",
        article: "文章"
      },
      steps: {
        compare: "先看套餐对比",
        simulator: "使用费用计算器",
        requirements: "确认签约条件",
        faq: "阅读常见问题",
        howto: "查看申请步骤",
        apply: "打开官方链接"
      }
    },
    "zh-TW": {
      badge: "建議閱讀順序",
      defaultTitle: "建議從這裡開始。",
      fromSource: "如果你是從{source}進來的，建議先看這裡。",
      body: "為了讓這頁真正有用，建議照這個順序閱讀：先比較，再確認申辦條件，只有當你覺得Rakuten真的最適合時，再打開官方員工推薦連結。",
      note: "員工推薦獎勵已在最後區塊清楚揭露，這份指南也會直接說明哪些情況下Rakuten並不是最佳選擇。",
      ctaEyebrow: "只有在Rakuten仍然最適合你時，再打開這個官方連結",
      ctaTitle: "如果比較後你仍然覺得Rakuten最適合，可以在這裡申辦",
      ctaText: "這是官方員工推薦連結，會自動套用推薦方案。但只有在Rakuten比上面的其他選項更適合你的地區、預算與開通需求時，才建議使用。",
      ctaButton: "打開官方推薦連結 →",
      sources: {
        reddit: "Reddit",
        quora: "Quora",
        devto: "dev.to",
        hashnode: "Hashnode",
        threads: "Threads",
        search: "搜尋",
        article: "文章"
      },
      steps: {
        compare: "先看方案比較",
        simulator: "使用費用計算器",
        requirements: "確認申辦條件",
        faq: "閱讀常見問題",
        howto: "查看申辦步驟",
        apply: "打開官方連結"
      }
    },
    vi: {
      badge: "Lối đi đề xuất",
      defaultTitle: "Nên bắt đầu từ đây.",
      fromSource: "Nếu bạn đến từ {source}, hãy bắt đầu ở đây.",
      body: "Để trang này thực sự hữu ích, hãy đi theo thứ tự này: so sánh trước, kiểm tra điều kiện đăng ký sau, và chỉ mở link giới thiệu chính thức nếu Rakuten vẫn là lựa chọn phù hợp nhất.",
      note: "Khoản khích lệ giới thiệu đã được công khai ở phần cuối, và hướng dẫn này cũng nói rõ khi nào Rakuten không phải lựa chọn tốt nhất.",
      ctaEyebrow: "Chỉ mở link chính thức này nếu Rakuten vẫn là lựa chọn phù hợp nhất",
      ctaTitle: "Nếu sau khi so sánh bạn vẫn thấy Rakuten phù hợp, bạn có thể đăng ký tại đây",
      ctaText: "Đây là link giới thiệu chính thức của nhân viên. Link này tự động áp dụng chương trình giới thiệu, nhưng bạn chỉ nên dùng nếu Rakuten phù hợp hơn các lựa chọn ở trên về khu vực sống, ngân sách và cách đăng ký.",
      ctaButton: "Mở link giới thiệu chính thức →",
      sources: {
        reddit: "Reddit",
        quora: "Quora",
        devto: "dev.to",
        hashnode: "Hashnode",
        threads: "Threads",
        search: "tìm kiếm",
        article: "bài viết"
      },
      steps: {
        compare: "So sánh gói cước",
        simulator: "Dùng bộ tính chi phí",
        requirements: "Kiểm tra điều kiện đăng ký",
        faq: "Đọc câu hỏi thường gặp",
        howto: "Xem các bước đăng ký",
        apply: "Mở link chính thức"
      }
    },
    tl: {
      badge: "Inirerekomendang daan",
      defaultTitle: "Dito muna magsimula.",
      fromSource: "Kung galing ka sa {source}, dito ka muna magsimula.",
      body: "Para manatiling kapaki-pakinabang ang page na ito, sundin ang ayos na ito: magkumpara muna, tingnan ang mga requirement pagkatapos, at buksan lang ang opisyal na referral link kung Rakuten pa rin ang pinakaangkop para sa iyo.",
      note: "Malinaw na nakasaad sa huling bahagi ang referral incentive, at sinasabi rin ng gabay na ito kung kailan hindi angkop ang Rakuten.",
      ctaEyebrow: "Opisyal na link, kung Rakuten pa rin ang pinakaangkop para sa iyo",
      ctaTitle: "Kung tama pa rin ang Rakuten matapos ikumpara, puwede kang mag-apply dito",
      ctaText: "Ito ang opisyal na employee referral link. Awtomatiko nitong ilalapat ang referral program, pero gamitin mo lang ito kung mas angkop ang Rakuten sa iyong lugar, budget, at setup needs kaysa sa mga alternatibo sa itaas.",
      ctaButton: "Buksan ang opisyal na referral link →",
      sources: {
        reddit: "Reddit",
        quora: "Quora",
        devto: "dev.to",
        hashnode: "Hashnode",
        threads: "Threads",
        search: "search",
        article: "artikulo"
      },
      steps: {
        compare: "Ihambing ang mga plan",
        simulator: "Gamitin ang cost calculator",
        requirements: "Tingnan ang requirements",
        faq: "Basahin ang FAQ",
        howto: "Tingnan ang signup steps",
        apply: "Buksan ang opisyal na link"
      }
    },
    es: {
      badge: "Ruta recomendada",
      defaultTitle: "Empieza aquí.",
      fromSource: "Si vienes de {source}, empieza aquí.",
      body: "Para que esta guía siga siendo útil, sigue este orden: compara primero, revisa los requisitos después y abre el enlace oficial de referido solo si Rakuten sigue siendo la mejor opción para ti.",
      note: "El incentivo por referido está claramente divulgado en la sección final, y esta guía también explica cuándo Rakuten no es la mejor opción.",
      ctaEyebrow: "Enlace oficial, solo si Rakuten sigue siendo la mejor opción para ti",
      ctaTitle: "Si después de comparar Rakuten te sigue encajando, puedes solicitarlo aquí",
      ctaText: "Este es el enlace oficial de referido de empleado. Aplica el programa automáticamente, pero solo deberías usarlo si Rakuten encaja mejor que las alternativas anteriores para tu zona, tu presupuesto y tu forma de contratar.",
      ctaButton: "Abrir enlace oficial de referido →",
      sources: {
        reddit: "Reddit",
        quora: "Quora",
        devto: "dev.to",
        hashnode: "Hashnode",
        threads: "Threads",
        search: "búsqueda",
        article: "un artículo"
      },
      steps: {
        compare: "Comparar planes",
        simulator: "Usar la calculadora",
        requirements: "Revisar requisitos",
        faq: "Leer el FAQ",
        howto: "Ver pasos de alta",
        apply: "Abrir enlace oficial"
      }
    },
    id: {
      badge: "Rute yang disarankan",
      defaultTitle: "Mulai dari sini.",
      fromSource: "Kalau datang dari {source}, mulai dari sini.",
      body: "Agar halaman ini tetap berguna, ikuti urutan ini: bandingkan dulu, cek syarat pendaftaran setelah itu, dan buka link referral resmi hanya jika Rakuten masih terasa paling cocok untuk Anda.",
      note: "Insentif referral sudah dijelaskan dengan jelas di bagian akhir, dan panduan ini juga menjelaskan kapan Rakuten bukan pilihan terbaik.",
      ctaEyebrow: "Link resmi, hanya jika Rakuten masih paling cocok untuk Anda",
      ctaTitle: "Kalau setelah membandingkan Rakuten masih paling cocok, Anda bisa daftar di sini",
      ctaText: "Ini adalah link referral resmi karyawan. Link ini otomatis menerapkan program referral, tetapi sebaiknya dipakai hanya jika Rakuten lebih cocok daripada alternatif di atas untuk area, anggaran, dan kebutuhan setup Anda.",
      ctaButton: "Buka link referral resmi →",
      sources: {
        reddit: "Reddit",
        quora: "Quora",
        devto: "dev.to",
        hashnode: "Hashnode",
        threads: "Threads",
        search: "pencarian",
        article: "artikel"
      },
      steps: {
        compare: "Bandingkan paket",
        simulator: "Pakai kalkulator biaya",
        requirements: "Cek syarat pendaftaran",
        faq: "Baca FAQ",
        howto: "Lihat langkah pendaftaran",
        apply: "Buka link resmi"
      }
    },
    ne: {
      badge: "सिफारिस गरिएको क्रम",
      defaultTitle: "यहाँबाट सुरु गर्नुहोस्।",
      fromSource: "यदि तपाईं {source} बाट आउनुभएको हो भने, यहाँबाट सुरु गर्नुहोस्।",
      body: "यो पेज उपयोगी रहोस् भन्ने हो भने यो क्रम पालना गर्नुहोस्: पहिले तुलना, त्यसपछि दर्ता आवश्यकताहरू, र Rakuten नै सबैभन्दा उपयुक्त देखिएपछि मात्र आधिकारिक रेफरल लिंक खोल्नुहोस्।",
      note: "रेफरल प्रोत्साहन अन्तिम भागमा खुला रूपमा उल्लेख गरिएको छ, र यो गाइडले Rakuten उपयुक्त नहुने अवस्थाहरू पनि स्पष्ट बताउँछ।",
      ctaEyebrow: "Rakuten अझै पनि तपाईंका लागि सबैभन्दा उपयुक्त देखिएमा मात्र खोल्ने आधिकारिक लिंक",
      ctaTitle: "तुलना गरेपछि पनि Rakuten उपयुक्त लागेमा, यहाँबाट दर्ता गर्न सक्नुहुन्छ",
      ctaText: "यो आधिकारिक कर्मचारी रेफरल लिंक हो। यसले रेफरल कार्यक्रम स्वतः लागू गर्छ, तर माथिका विकल्पहरूभन्दा Rakuten तपाईंको क्षेत्र, बजेट र सेटअप आवश्यकतामा बढी उपयुक्त भएमा मात्र प्रयोग गर्नुहोस्।",
      ctaButton: "आधिकारिक रेफरल लिंक खोल्नुहोस् →",
      sources: {
        reddit: "Reddit",
        quora: "Quora",
        devto: "dev.to",
        hashnode: "Hashnode",
        threads: "Threads",
        search: "खोज",
        article: "लेख"
      },
      steps: {
        compare: "प्लान तुलना हेर्नुहोस्",
        simulator: "खर्च क्याल्कुलेटर प्रयोग गर्नुहोस्",
        requirements: "दर्ता आवश्यकताहरू जाँच्नुहोस्",
        faq: "FAQ पढ्नुहोस्",
        howto: "दर्ता चरणहरू हेर्नुहोस्",
        apply: "आधिकारिक लिंक खोल्नुहोस्"
      }
    },
    pt: {
      badge: "Caminho sugerido",
      defaultTitle: "Comece por aqui.",
      fromSource: "Se você veio do {source}, comece por aqui.",
      body: "Para manter esta página útil, siga esta ordem: compare primeiro, confira os requisitos depois e abra o link oficial de indicação só se a Rakuten continuar parecendo a melhor opção para você.",
      note: "O incentivo de indicação está divulgado de forma clara na parte final, e este guia também explica quando a Rakuten não é a melhor escolha.",
      ctaEyebrow: "Link oficial, somente se a Rakuten ainda parecer a melhor opção para você",
      ctaTitle: "Se depois de comparar a Rakuten ainda fizer sentido, você pode contratar aqui",
      ctaText: "Este é o link oficial de indicação de funcionário. Ele aplica o programa automaticamente, mas só deve ser usado se a Rakuten fizer mais sentido do que as alternativas acima para sua região, seu orçamento e sua forma de contratação.",
      ctaButton: "Abrir link oficial de indicação →",
      sources: {
        reddit: "Reddit",
        quora: "Quora",
        devto: "dev.to",
        hashnode: "Hashnode",
        threads: "Threads",
        search: "busca",
        article: "artigo"
      },
      steps: {
        compare: "Comparar planos",
        simulator: "Usar calculadora de custo",
        requirements: "Ver requisitos",
        faq: "Ler o FAQ",
        howto: "Ver etapas de cadastro",
        apply: "Abrir link oficial"
      }
    },
    th: {
      badge: "เส้นทางที่แนะนำ",
      defaultTitle: "เริ่มจากตรงนี้",
      fromSource: "ถ้ามาจาก {source} ให้เริ่มตรงนี้",
      body: "เพื่อให้หน้านี้ยังคงมีประโยชน์ แนะนำให้ดูตามลำดับนี้ก่อน: เปรียบเทียบก่อน ตรวจเงื่อนไขการสมัครถัดไป แล้วค่อยเปิดลิงก์แนะนำอย่างเป็นทางการเมื่อคุณยังคิดว่า Rakuten เหมาะที่สุด",
      note: "มีการเปิดเผยแรงจูงใจจาก referral ไว้อย่างชัดเจนในส่วนท้าย และคู่มือนี้ก็อธิบายตรง ๆ ด้วยว่าเมื่อไร Rakuten ไม่ใช่ตัวเลือกที่ดีที่สุด",
      ctaEyebrow: "ลิงก์ทางการที่ควรเปิดก็ต่อเมื่อ Rakuten ยังเป็นตัวเลือกที่เหมาะที่สุดสำหรับคุณ",
      ctaTitle: "ถ้าเปรียบเทียบแล้ว Rakuten ยังเหมาะที่สุด คุณสมัครต่อได้ที่นี่",
      ctaText: "นี่คือลิงก์แนะนำพนักงานอย่างเป็นทางการ ระบบจะใช้โปรแกรมแนะนำให้อัตโนมัติ แต่ควรใช้ก็ต่อเมื่อ Rakuten เหมาะกับพื้นที่ งบประมาณ และวิธีสมัครของคุณมากกว่าทางเลือกด้านบน",
      ctaButton: "เปิดลิงก์แนะนำอย่างเป็นทางการ →",
      sources: {
        reddit: "Reddit",
        quora: "Quora",
        devto: "dev.to",
        hashnode: "Hashnode",
        threads: "Threads",
        search: "การค้นหา",
        article: "บทความ"
      },
      steps: {
        compare: "ดูการเปรียบเทียบแพ็กเกจ",
        simulator: "ใช้เครื่องคำนวณค่าใช้จ่าย",
        requirements: "ตรวจเงื่อนไขการสมัคร",
        faq: "อ่าน FAQ",
        howto: "ดูขั้นตอนสมัคร",
        apply: "เปิดลิงก์ทางการ"
      }
    }
  };

  var SOURCE_LABELS = {
    bluesky: "Bluesky"
  };

  var SOURCE_FLOW = {
    reddit: ["faq", "requirements", "compare"],
    quora: ["requirements", "faq", "compare"],
    threads: ["compare", "simulator", "apply"],
    bluesky: ["compare", "requirements", "apply"],
    article: ["compare", "howto", "apply"],
    search: ["compare", "simulator", "requirements"],
    direct: ["compare", "requirements", "apply"]
  };

  function init() {
    var lang = resolveLang();
    var copy = COPY[lang] || COPY.en;
    var hero = document.querySelector(".hero");
    if (!hero) {
      return;
    }

    ensureSectionIds();

    var source = detectSource();
    if (!source || !source.category) {
      source = { category: "direct", labelKey: "direct", persist: null };
    }

    syncSourceParam(source);
    preserveSourceOnInternalLinks(source.persist);
    injectEntryPath(hero, copy, source);
    tuneCallToAction(copy);
  }

  function resolveLang() {
    var raw = document.documentElement.getAttribute("lang") || "en";
    if (COPY[raw]) {
      return raw;
    }
    if (raw.toLowerCase().indexOf("zh-tw") === 0) {
      return "zh-TW";
    }
    if (raw.toLowerCase().indexOf("zh-hant") === 0) {
      return "zh-TW";
    }
    if (raw.toLowerCase().indexOf("zh") === 0) {
      return "zh-Hans";
    }
    return "en";
  }

  function ensureSectionIds() {
    var cta = document.querySelector(".cta-section, .cta, .cta2, .cta-sec");
    if (cta && !cta.id) {
      cta.id = "apply";
    }

    var sections = Array.prototype.slice.call(document.querySelectorAll("section, sec"));
    if (!sections.length) {
      return;
    }

    var ordered = sections.filter(function (el) {
      return !el.closest(".cta-section, .cta, .cta2, .cta-sec");
    });

    if (!document.getElementById("compare") && ordered[0]) {
      ordered[0].id = "compare";
    }
    if (!document.getElementById("simulator") && !document.getElementById("sim") && ordered[1]) {
      ordered[1].id = "simulator";
    }
    if (!document.getElementById("rakuten") && ordered[2]) {
      ordered[2].id = "rakuten";
    }
    if (!document.getElementById("faq") && ordered[3]) {
      ordered[3].id = "faq";
    }
    if (!document.getElementById("points") && ordered[4]) {
      ordered[4].id = "points";
    }
    if (!document.getElementById("requirements") && ordered[5]) {
      ordered[5].id = "requirements";
    }
    if (!document.getElementById("howto") && ordered[6]) {
      ordered[6].id = "howto";
    }
  }

  function detectSource() {
    var params = new URLSearchParams(window.location.search);
    var explicit = params.get("src") || params.get("utm_source") || params.get("ref");
    if (explicit) {
      return classifySource(explicit);
    }

    if (!document.referrer) {
      return { category: "direct", labelKey: "direct", persist: null };
    }

    try {
      var refUrl = new URL(document.referrer);
      return classifyReferrer(refUrl.hostname.toLowerCase());
    } catch (err) {
      return { category: "direct", labelKey: "direct", persist: null };
    }
  }

  function classifySource(raw) {
    var value = String(raw || "").toLowerCase();

    if (value.indexOf("reddit") !== -1) {
      return { category: "reddit", labelKey: "reddit", persist: "reddit" };
    }
    if (value.indexOf("quora") !== -1) {
      return { category: "quora", labelKey: "quora", persist: "quora" };
    }
    if (value.indexOf("hashnode") !== -1) {
      return { category: "article", labelKey: "hashnode", persist: "hashnode" };
    }
    if (value.indexOf("dev") !== -1) {
      return { category: "article", labelKey: "devto", persist: "devto" };
    }
    if (value.indexOf("article") !== -1 || value.indexOf("blog") !== -1) {
      return { category: "article", labelKey: "article", persist: "article" };
    }
    if (value.indexOf("thread") !== -1) {
      return { category: "threads", labelKey: "threads", persist: "threads" };
    }
    if (value.indexOf("bluesky") !== -1 || value.indexOf("bsky") !== -1) {
      return { category: "bluesky", labelKey: "bluesky", persist: "bluesky" };
    }
    if (
      value.indexOf("google") !== -1 ||
      value.indexOf("bing") !== -1 ||
      value.indexOf("yahoo") !== -1 ||
      value.indexOf("duckduckgo") !== -1 ||
      value.indexOf("search") !== -1
    ) {
      return { category: "search", labelKey: "search", persist: "search" };
    }

    return { category: "direct", labelKey: "direct", persist: null };
  }

  function classifyReferrer(hostname) {
    if (hostname.indexOf("reddit.com") !== -1) {
      return { category: "reddit", labelKey: "reddit", persist: "reddit" };
    }
    if (hostname.indexOf("quora.com") !== -1) {
      return { category: "quora", labelKey: "quora", persist: "quora" };
    }
    if (hostname.indexOf("dev.to") !== -1) {
      return { category: "article", labelKey: "devto", persist: "devto" };
    }
    if (hostname.indexOf("hashnode") !== -1) {
      return { category: "article", labelKey: "hashnode", persist: "hashnode" };
    }
    if (hostname.indexOf("threads.net") !== -1) {
      return { category: "threads", labelKey: "threads", persist: "threads" };
    }
    if (hostname.indexOf("bsky.app") !== -1 || hostname.indexOf("bsky.social") !== -1) {
      return { category: "bluesky", labelKey: "bluesky", persist: "bluesky" };
    }
    if (
      hostname.indexOf("google.") !== -1 ||
      hostname.indexOf("bing.com") !== -1 ||
      hostname.indexOf("duckduckgo.com") !== -1 ||
      hostname.indexOf("search.yahoo.com") !== -1
    ) {
      return { category: "search", labelKey: "search", persist: "search" };
    }
    return { category: "direct", labelKey: "direct", persist: null };
  }

  function syncSourceParam(source) {
    if (!source || !source.persist) {
      return;
    }
    var url = new URL(window.location.href);
    if (!url.searchParams.get("src")) {
      url.searchParams.set("src", source.persist);
      window.history.replaceState(null, "", url.toString());
    }
  }

  function preserveSourceOnInternalLinks(persist) {
    if (!persist) {
      return;
    }

    var anchors = Array.prototype.slice.call(document.querySelectorAll("a[href]"));
    anchors.forEach(function (anchor) {
      var href = anchor.getAttribute("href");
      if (!href || href.charAt(0) === "#" || href.indexOf("mailto:") === 0 || href.indexOf("tel:") === 0) {
        return;
      }

      var url;
      try {
        url = new URL(href, window.location.href);
      } catch (err) {
        return;
      }

      if (url.origin !== window.location.origin) {
        return;
      }
      if (url.pathname.indexOf("/japan-sim-guide/") !== 0) {
        return;
      }
      if (url.pathname === window.location.pathname && url.hash) {
        return;
      }

      if (!url.searchParams.get("src")) {
        url.searchParams.set("src", persist);
      }

      anchor.setAttribute("href", url.pathname + url.search + url.hash);
    });
  }

  function injectEntryPath(hero, copy, source) {
    if (document.querySelector(".entry-path")) {
      return;
    }

    var flowKeys = SOURCE_FLOW[source.category] || SOURCE_FLOW.direct;
    var steps = buildStepLinks(flowKeys, copy, source.persist);
    if (!steps.length) {
      return;
    }

    var sourceName = copy.sources[source.labelKey] || SOURCE_LABELS[source.labelKey] || copy.sources.article;
    var title = source.category === "direct"
      ? copy.defaultTitle
      : copy.fromSource.replace("{source}", sourceName);

    var wrapper = document.createElement("section");
    wrapper.className = "entry-path";

    var stepsHtml = steps.map(function (step, index) {
      return (
        '<a class="entry-path-step" href="' +
        escapeAttr(step.href) +
        '">' +
        '<span class="entry-path-step-num">' +
        (index + 1) +
        "</span>" +
        '<span class="entry-path-step-text">' +
        escapeHtml(step.label) +
        "</span>" +
        "</a>"
      );
    }).join("");

    wrapper.innerHTML =
      '<div class="entry-path-card">' +
      '<div class="entry-path-kicker">' + escapeHtml(copy.badge) + "</div>" +
      '<h2 class="entry-path-title">' + escapeHtml(title) + "</h2>" +
      '<p class="entry-path-body">' + escapeHtml(copy.body) + "</p>" +
      '<div class="entry-path-steps">' + stepsHtml + "</div>" +
      '<p class="entry-path-note">' + escapeHtml(copy.note) + "</p>" +
      "</div>";

    hero.insertAdjacentElement("afterend", wrapper);
  }

  function buildStepLinks(flowKeys, copy, persist) {
    var chosen = [];
    flowKeys.forEach(function (key) {
      var href = hrefFor(key, persist);
      if (href && copy.steps[key]) {
        chosen.push({ key: key, href: href, label: copy.steps[key] });
      }
    });

    if (chosen.length >= 3) {
      return chosen.slice(0, 3);
    }

    var fallback = SOURCE_FLOW.direct;
    fallback.forEach(function (key) {
      if (chosen.length >= 3) {
        return;
      }
      var already = chosen.some(function (step) { return step.key === key; });
      var href = hrefFor(key, persist);
      if (!already && href && copy.steps[key]) {
        chosen.push({ key: key, href: href, label: copy.steps[key] });
      }
    });

    return chosen.slice(0, 3);
  }

  function hrefFor(key) {
    if (key === "compare" && document.getElementById("compare")) {
      return "#compare";
    }
    if (key === "simulator") {
      if (document.getElementById("simulator")) {
        return "#simulator";
      }
      if (document.getElementById("sim")) {
        return "#sim";
      }
    }
    if (key === "requirements" && document.getElementById("requirements")) {
      return "#requirements";
    }
    if (key === "faq" && document.getElementById("faq")) {
      return "#faq";
    }
    if (key === "howto" && document.getElementById("howto")) {
      return "#howto";
    }
    if (key === "apply") {
      var cta = document.getElementById("apply");
      if (cta) {
        return "#apply";
      }
    }
    return null;
  }

  function tuneCallToAction(copy) {
    var cta = document.querySelector(".cta-section, .cta, .cta2, .cta-sec");
    if (!cta) {
      return;
    }
    if (!cta.id) {
      cta.id = "apply";
    }

    var heading = cta.querySelector("h2");
    var eyebrow = cta.querySelector(".cta-eyebrow, .cta-ey, .ce");
    if (!eyebrow && heading) {
      eyebrow = document.createElement("p");
      eyebrow.className = "entry-cta-kicker";
      heading.parentNode.insertBefore(eyebrow, heading);
    }

    if (eyebrow) {
      eyebrow.textContent = copy.ctaEyebrow;
    }
    if (heading) {
      heading.textContent = copy.ctaTitle;
    }

    var lead = Array.prototype.slice.call(cta.querySelectorAll("p")).find(function (paragraph) {
      return !paragraph.matches(".cta-disclosure, .cta-dis, .cd, .ce, .entry-cta-kicker, .cta-eyebrow, .cta-ey");
    });
    if (lead) {
      lead.textContent = copy.ctaText;
    }

    var button = cta.querySelector("a");
    if (button) {
      button.textContent = copy.ctaButton;
    }
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function escapeAttr(value) {
    return escapeHtml(value).replace(/"/g, "&quot;");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
